import { NextRequest, NextResponse } from 'next/server';
import { ChatOpenAI } from '@langchain/openai';
import { PromptTemplate } from '@langchain/core/prompts';
import { StructuredOutputParser } from 'langchain/output_parsers';
import pdfParse from 'pdf-parse';
import { z } from 'zod';

// 1. Define the desired output schema using Zod
const outputParser = StructuredOutputParser.fromZodSchema(
  z.object({
    score: z.number().min(0).max(100).describe('The overall ESG alignment score from 0 to 100, where 100 is perfect alignment.'),
    summary: z.string().describe("A 2-3 sentence executive summary of the bank's ESG posture based on the report."),
    gaps: z.array(
      z.object({
        area: z.string().describe('The specific area of non-compliance or weakness (e.g., "CSRD Double Materiality", "EU Taxonomy DNSH").'),
        description: z.string().describe('A detailed description of the identified gap.'),
        recommendation: z.string().describe('A concrete, actionable recommendation to close the gap.'),
      })
    ).describe('An array of identified gaps and recommendations.'),
  })
);

// 2. Create the prompt template
const promptTemplate = new PromptTemplate({
  template: `You are "ESG Copilot," an expert AI assistant specializing in European banking regulations and sustainability. Your task is to analyze a bank's ESG report against a specific EU framework.

  **Instructions:**
  1.  Carefully read the provided text from the bank's ESG report.
  2.  Compare it against the key requirements of the "{framework}" framework.
  3.  Calculate an alignment score from 0-100.
  4.  Provide a concise summary.
  5.  Identify specific gaps and provide actionable recommendations for each.
  6.  Format your entire output as a JSON object that strictly follows the provided schema.

  {format_instructions}

  **Framework for Analysis:** {framework}

  **Bank's ESG Report Text:**
  ---
  {report_text}
  ---
  `,
  inputVariables: ['framework', 'report_text'],
  partialVariables: { format_instructions: outputParser.getFormatInstructions() },
});

// 3. The main API function
export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File | null;
    const framework = formData.get('framework') as string | null;

    if (!file || !framework) {
      return NextResponse.json({ error: 'File and framework are required.' }, { status: 400 });
    }

    // Read the PDF file
    const fileBuffer = Buffer.from(await file.arrayBuffer());
    const pdfData = await pdfParse(fileBuffer);
    const reportText = pdfData.text;

    // Truncate for safety and cost control (adjust as needed)
    const truncatedText = reportText.slice(0, 15000);

    const model = new ChatOpenAI({
      modelName: 'gpt-4-turbo-preview', // Powerful model for this task
      temperature: 0.2, // Low temperature for factual, consistent output
    });

    const input = await promptTemplate.format({
      framework: framework,
      report_text: truncatedText,
    });

    const response = await model.invoke(input);
    const parsedResponse = await outputParser.parse(response.content as string);

    return NextResponse.json(parsedResponse, { status: 200 });

  } catch (error) {
    console.error('Error in analysis API:', error);
    const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
    return NextResponse.json({ error: 'Failed to analyze the document.', details: errorMessage }, { status: 500 });
  }
} 