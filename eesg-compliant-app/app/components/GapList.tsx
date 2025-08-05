import { AlertTriangle, Lightbulb, TrendingUp } from 'lucide-react';

export interface Gap {
  area: string;
  description: string;
  recommendation: string;
}

interface GapListProps {
  gaps: Gap[];
}

const GapList = ({ gaps }: GapListProps) => {
  if (!gaps || gaps.length === 0) {
    return (
      <div className="bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-green-400/30 text-center">
        <div className="relative">
          <Lightbulb className="mx-auto h-16 w-16 text-success mb-4" />
          <div className="absolute inset-0 bg-success/20 rounded-full animate-ping"></div>
        </div>
        <h3 className="text-2xl font-bold text-white mb-2">No Gaps Found!</h3>
        <p className="text-white/70 text-lg">Excellent alignment with the selected framework.</p>
      </div>
    );
  }

  return (
    <div className="bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/20 w-full space-y-6">
      <div className="flex items-center gap-3 mb-6">
        <TrendingUp className="h-8 w-8 text-warning" />
        <h3 className="text-2xl font-bold text-white">Improvement Areas</h3>
      </div>
      {gaps.map((gap, index) => (
        <div 
          key={index} 
          className="border-l-4 border-warning p-6 bg-warning/10 backdrop-blur-sm rounded-r-xl hover:bg-warning/20 transition-all duration-300 hover:scale-[1.02]"
        >
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-8 w-8 text-warning" />
            </div>
            <div className="flex-1">
              <h4 className="text-xl font-bold text-white mb-3">{gap.area}</h4>
              <p className="text-white/80 leading-relaxed mb-4">{gap.description}</p>
            </div>
          </div>
          <div className="mt-4 flex items-start space-x-4 pl-4 border-t pt-4 border-warning/30">
            <div className="flex-shrink-0">
              <Lightbulb className="h-6 w-6 text-success" />
            </div>
            <div className="flex-1">
              <h5 className="font-semibold text-lg text-success mb-2">Recommendation</h5>
              <p className="text-success/90 leading-relaxed">{gap.recommendation}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default GapList; 