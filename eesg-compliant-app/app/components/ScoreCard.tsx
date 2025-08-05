// app/components/ScoreCard.tsx
import { Target } from 'lucide-react';

interface ScoreCardProps {
  score: number;
  summary: string;
}

const ScoreCard = ({ score, summary }: ScoreCardProps) => {
  const getScoreColor = () => {
    if (score >= 80) return 'text-success';
    if (score >= 50) return 'text-warning';
    return 'text-error';
  };

  const getScoreStatus = () => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  };

  return (
    <div className="bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/20 p-8 w-full">
      <div className="flex items-start space-x-6">
        <div className="flex-shrink-0">
          <div className={`flex items-center justify-center h-20 w-20 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 ${getScoreColor()}`}>
            <Target size={40} className="text-white" />
          </div>
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-4">
            <h3 className="text-2xl font-bold text-white">ESG Alignment Score</h3>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreColor()} bg-white/10 backdrop-blur-sm`}>
              {getScoreStatus()}
            </span>
          </div>
          <p className={`text-6xl font-bold ${getScoreColor()} mb-4`}>
            {score}<span className="text-3xl">%</span>
          </p>
          <p className="text-lg text-white/80 leading-relaxed">
            {summary}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ScoreCard; 