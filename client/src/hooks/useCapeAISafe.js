import { useContext } from 'react';
import { CapeAIContext } from '../context/CapeAIContextSafe';

export default function useCapeAISafe() {
  const context = useContext(CapeAIContext);
  
  // Return safe defaults if context is not available
  if (!context || !context.isInitialized) {
    return {
      isVisible: false,
      messages: [],
      onboardingStep: 0,
      onboardingData: {
        profileComplete: false,
        featuresViewed: false,
        aiIntroduced: false,
        dashboardTour: false,
        firstAgentLaunched: false,
      },
      toggleVisibility: () => console.warn('CapeAI not initialized'),
      addMessage: () => console.warn('CapeAI not initialized'),
      setOnboardingStep: () => console.warn('CapeAI not initialized'),
      updateOnboardingData: () => console.warn('CapeAI not initialized'),
      isInitialized: false,
    };
  }
  
  return context;
}
