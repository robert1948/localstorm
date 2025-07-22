import { useContext } from 'react';
import { CapeAIContext } from '../context/CapeAIContextSafe';

export default function useCapeAISafe() {
  try {
    const context = useContext(CapeAIContext);
    
    // Return safe defaults if context is not available or not initialized
    if (!context) {
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
        toggleVisibility: () => console.warn('CapeAI not available'),
        addMessage: () => console.warn('CapeAI not available'),
        setOnboardingStep: () => console.warn('CapeAI not available'),
        updateOnboardingData: () => console.warn('CapeAI not available'),
        isInitialized: false,
      };
    }
    
    return context;
  } catch (error) {
    console.warn('CapeAI context error:', error);
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
      toggleVisibility: () => {},
      addMessage: () => {},
      setOnboardingStep: () => {},
      updateOnboardingData: () => {},
      isInitialized: false,
    };
  }
}
