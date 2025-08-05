"use client";

import { useState, useEffect } from 'react';
import Image from 'next/image';
import { UploadCloud, Loader2, BarChart, FileText, X, Sparkles, Zap, Shield, TrendingUp, Globe, Brain, CheckCircle, Target, BarChart3 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ScoreCard from './components/ScoreCard';
import GapList, { Gap } from './components/GapList';

interface AnalysisResult {
  score: number;
  summary: string;
  gaps: Gap[];
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [selectedFramework, setSelectedFramework] = useState('CSRD');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
      setAnalysisResult(null);
      setError(null);
    }
  };

  const handleFileDrop = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        if (e.dataTransfer.files[0].type === "application/pdf") {
            setFile(e.dataTransfer.files[0]);
            setAnalysisResult(null);
            setError(null);
        } else {
            setError("Please upload a PDF file.");
        }
    }
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) {
      setError('Please upload a PDF file first.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);

    // Simulate API call with mock data
    setTimeout(() => {
      const mockResult = {
        score: 75,
        summary: "This is a mock analysis result showing good ESG alignment with some areas for improvement.",
        gaps: [
          {
            area: "CSRD Double Materiality",
            description: "The report lacks comprehensive double materiality assessment.",
            recommendation: "Implement a structured double materiality assessment process."
          },
          {
            area: "EU Taxonomy DNSH",
            description: "Insufficient evidence of Do No Significant Harm criteria compliance.",
            recommendation: "Develop detailed DNSH assessment framework and reporting."
          }
        ]
      };
      setAnalysisResult(mockResult);
      setIsLoading(false);
    }, 3000);
  };

  return (
    <div className="min-h-screen w-full relative overflow-hidden">
      {/* Premium Aurora Background */}
      <div className="fixed inset-0 bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,hsla(165,100%,36%,0.3)_0px,transparent_50%),radial-gradient(circle_at_80%_20%,hsla(210,89%,20%,0.3)_0px,transparent_50%),radial-gradient(circle_at_20%_80%,hsla(43,89%,50%,0.2)_0px,transparent_50%),radial-gradient(circle_at_80%_80%,hsla(210,89%,20%,0.3)_0px,transparent_50%)] animate-aurora"></div>
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNGRkYiIGZpbGwtb3BhY2l0eT0iMC4wMiI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMiIvPjwvZz48L2c+PC9zdmc+')] opacity-30"></div>
      </div>

      {/* Floating Aurora Particles */}
      <div className="fixed inset-0 pointer-events-none">
        <motion.div
          animate={{ 
            y: [0, -30, 0],
            x: [0, 20, 0],
            opacity: [0.3, 0.8, 0.3]
          }}
          transition={{ 
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute top-20 left-10 w-6 h-6 bg-blue-400/40 rounded-full blur-sm"
        />
        <motion.div
          animate={{ 
            y: [0, 40, 0],
            x: [0, -30, 0],
            opacity: [0.2, 0.6, 0.2]
          }}
          transition={{ 
            duration: 12,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 2
          }}
          className="absolute top-40 right-20 w-8 h-8 bg-purple-400/30 rounded-full blur-sm"
        />
        <motion.div
          animate={{ 
            x: [0, 25, 0],
            y: [0, -20, 0],
            opacity: [0.4, 0.7, 0.4]
          }}
          transition={{ 
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 4
          }}
          className="absolute bottom-40 left-20 w-4 h-4 bg-green-400/50 rounded-full blur-sm"
        />
        <motion.div
          animate={{ 
            y: [0, -15, 0],
            x: [0, -25, 0],
            opacity: [0.3, 0.6, 0.3]
          }}
          transition={{ 
            duration: 15,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 6
          }}
          className="absolute bottom-20 right-40 w-5 h-5 bg-cyan-400/40 rounded-full blur-sm"
        />
      </div>

      <main className="relative container mx-auto px-4 py-8 md:py-16 z-10">
        {/* Premium Header with Larger Logo */}
        <motion.header 
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="text-center mb-20"
        >
          {/* Premium ESG Logo */}
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="relative mb-12"
          >
            <div className="relative w-48 h-48 mx-auto">
              {/* Outer glow */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500 via-purple-500 to-green-500 rounded-full shadow-2xl animate-pulse blur-xl opacity-50"></div>
              
              {/* Main logo container */}
              <div className="absolute inset-4 bg-gradient-to-br from-blue-600 via-purple-600 to-green-600 rounded-full shadow-2xl"></div>
              
              {/* Logo content */}
              <div className="absolute inset-8 flex items-center justify-center">
                <div className="relative">
                  {/* ESG Letters */}
                  <div className="text-white font-bold text-4xl mb-2">
                    <span className="text-blue-200">E</span>
                    <span className="text-green-200">S</span>
                    <span className="text-purple-200">G</span>
                  </div>
                  
                  {/* Compliance Icon */}
                  <div className="flex justify-center mb-3">
                    <div className="relative">
                      <BarChart3 className="w-12 h-12 text-white" />
                      <CheckCircle className="w-6 h-6 text-green-300 absolute -top-1 -right-1" />
                    </div>
                  </div>
                  
                  {/* Target indicator */}
                  <div className="flex justify-center">
                    <Target className="w-8 h-8 text-yellow-300" />
                  </div>
                </div>
              </div>
              
              {/* Animated ring */}
              <motion.div
                animate={{ 
                  rotate: 360
                }}
                transition={{ 
                  duration: 20,
                  repeat: Infinity,
                  ease: "linear"
                }}
                className="absolute inset-0 border-2 border-white/20 rounded-full"
              />
            </div>
          </motion.div>

          {/* Premium Title */}
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="text-7xl md:text-8xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent mb-8 drop-shadow-2xl"
          >
            ESG Copilot
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="text-2xl md:text-3xl text-blue-200 mb-12 font-light"
          >
            AI-Powered ESG Compliance Analysis
          </motion.p>

          {/* Simplified Feature Pills */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.7 }}
            className="flex items-center justify-center gap-6 text-lg"
          >
            <div className="flex items-center gap-3 bg-white/10 backdrop-blur-sm px-6 py-3 rounded-full border border-white/20">
              <Sparkles className="w-5 h-5 text-yellow-300" />
              <span className="text-white/90 font-medium">Advanced AI</span>
            </div>
            <div className="flex items-center gap-3 bg-white/10 backdrop-blur-sm px-6 py-3 rounded-full border border-white/20">
              <Shield className="w-5 h-5 text-green-300" />
              <span className="text-white/90 font-medium">Compliance</span>
            </div>
          </motion.div>
        </motion.header>

        <div className="max-w-5xl mx-auto">
          <AnimatePresence>
            {!analysisResult && (
              <motion.div
                key="form"
                initial={{ opacity: 0, scale: 0.9, y: 30 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.5 }}
                className="bg-white/10 backdrop-blur-xl p-10 rounded-3xl shadow-2xl border border-white/20"
              >
                <form onSubmit={handleSubmit} className="space-y-10">
                  {/* Premium File Upload */}
                  <div>
                    <label 
                      htmlFor="file-upload" 
                      onDrop={handleFileDrop} 
                      onDragOver={(e) => e.preventDefault()} 
                      className="group relative flex flex-col items-center justify-center w-full h-64 border-2 border-white/30 border-dashed rounded-2xl cursor-pointer bg-white/5 hover:bg-white/10 transition-all duration-300 hover:border-white/50 overflow-hidden"
                    >
                      <motion.div
                        whileHover={{ scale: 1.05 }}
                        className="flex flex-col items-center justify-center pt-5 pb-6 relative z-10"
                      >
                        <motion.div
                          animate={{ y: [0, -5, 0] }}
                          transition={{ duration: 2, repeat: Infinity }}
                          className="mb-6"
                        >
                          <UploadCloud className="w-16 h-16 text-blue-300" />
                        </motion.div>
                        <p className="mb-3 text-xl text-white/90">
                          <span className="font-semibold text-blue-300">Click to upload</span> or drag and drop
                        </p>
                        <p className="text-base text-white/60">ESG Report (PDF, max 20MB)</p>
                      </motion.div>
                      
                      {/* Aurora background effect */}
                      <motion.div
                        className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                        animate={{
                          backgroundPosition: ['0% 50%', '100% 50%', '0% 50%']
                        }}
                        transition={{
                          duration: 3,
                          repeat: Infinity,
                          ease: "linear"
                        }}
                      />
                      
                      <input id="file-upload" type="file" className="hidden" onChange={handleFileChange} accept=".pdf" />
                    </label>
                    
                    {file && (
                      <motion.div 
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="mt-6 flex items-center justify-between bg-green-500/20 backdrop-blur-sm text-green-200 p-5 rounded-xl border border-green-400/30"
                      >
                        <span className="flex items-center gap-3 text-lg">
                          <FileText size={20}/>
                          {file.name}
                        </span>
                        <button 
                          onClick={() => setFile(null)}
                          className="hover:bg-white/10 p-2 rounded-full transition-colors"
                        >
                          <X size={20}/>
                        </button>
                      </motion.div>
                    )}
                  </div>

                  {/* Premium Framework Selection */}
                  <div>
                    <label className="block text-xl font-semibold text-white mb-6 flex items-center gap-3">
                      <Shield className="w-6 h-6 text-blue-300" />
                      Select EU Framework
                    </label>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {['CSRD', 'EU Taxonomy', 'SFDR'].map((framework) => (
                        <motion.button
                          key={framework}
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          type="button"
                          onClick={() => setSelectedFramework(framework)}
                          className={`p-8 rounded-xl border-2 transition-all duration-300 ${
                            selectedFramework === framework
                              ? 'border-blue-400 bg-blue-500/20 text-blue-200 shadow-lg shadow-blue-500/25'
                              : 'border-white/20 bg-white/5 text-white/70 hover:border-white/40 hover:bg-white/10'
                          }`}
                        >
                          <div className="text-center">
                            <div className="text-xl font-semibold mb-3">{framework}</div>
                            <div className="text-sm opacity-70">
                              {framework === 'CSRD' && 'Corporate Sustainability Reporting'}
                              {framework === 'EU Taxonomy' && 'Environmental Classification'}
                              {framework === 'SFDR' && 'Sustainable Finance Disclosure'}
                            </div>
                          </div>
                        </motion.button>
                      ))}
                    </div>
                  </div>

                  {/* Premium Submit Button */}
                  <div>
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      type="submit"
                      disabled={isLoading || !file}
                      className="w-full group relative overflow-hidden bg-gradient-to-r from-blue-600 via-purple-600 to-green-600 hover:from-blue-500 hover:via-purple-500 hover:to-green-500 disabled:from-gray-600 disabled:via-gray-600 disabled:to-gray-600 text-white font-semibold py-5 px-10 rounded-2xl text-xl transition-all duration-300 disabled:scale-100 disabled:cursor-not-allowed shadow-2xl"
                    >
                      <div className="absolute inset-0 bg-gradient-to-r from-blue-400/20 via-purple-400/20 to-green-400/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                      <div className="relative flex items-center justify-center gap-4">
                        {isLoading ? (
                          <>
                            <Loader2 className="w-7 h-7 animate-spin" />
                            <span>Analyzing with AI...</span>
                          </>
                        ) : (
                          <>
                            <BarChart className="w-7 h-7" />
                            <span>Launch AI Analysis</span>
                            <Sparkles className="w-6 h-6 animate-pulse" />
                          </>
                        )}
                      </div>
                    </motion.button>
                  </div>
                  
                  {error && (
                    <motion.div 
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="mt-6 p-5 bg-red-500/20 backdrop-blur-sm rounded-xl border border-red-400/30"
                    >
                      <p className="text-red-200 text-center text-lg">{error}</p>
                    </motion.div>
                  )}
                </form>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Premium Loading Animation */}
          {isLoading && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center mt-20"
            >
              <div className="relative">
                <div className="w-32 h-32 border-4 border-blue-400/30 border-t-blue-400 rounded-full animate-spin mx-auto"></div>
                <div className="absolute inset-0 w-32 h-32 border-4 border-purple-400/30 border-t-purple-400 rounded-full animate-spin mx-auto" style={{ animationDelay: '-0.5s' }}></div>
                <div className="absolute inset-0 w-32 h-32 border-4 border-green-400/30 border-t-green-400 rounded-full animate-spin mx-auto" style={{ animationDelay: '-1s' }}></div>
              </div>
              <motion.p 
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="mt-8 text-2xl text-blue-200 font-medium"
              >
                AI is analyzing your document...
              </motion.p>
              <p className="mt-3 text-white/60 text-lg">This may take a few moments</p>
            </motion.div>
          )}

          {/* Premium Results Section */}
          <AnimatePresence>
            {analysisResult && (
              <motion.div
                key="results"
                initial={{ opacity: 0, scale: 0.95, y: 30 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="mt-20 space-y-10"
              >
                <ScoreCard score={analysisResult.score} summary={analysisResult.summary} />
                <GapList gaps={analysisResult.gaps} />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
