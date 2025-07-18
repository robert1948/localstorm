import React from 'react';

class ContextErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    // Check if this is a context-related error
    if (error?.message?.includes('useContext') || 
        error?.message?.includes('Provider') ||
        error?.message?.includes('Context')) {
      return { hasError: true, error };
    }
    // For other errors, let them bubble up
    throw error;
  }

  componentDidCatch(error, errorInfo) {
    console.warn('🛡️ Context Error Boundary caught error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Safe fallback when context fails
      return (
        <div className="p-4 text-center text-yellow-600 bg-yellow-50 rounded-lg border border-yellow-200">
          <p className="text-sm">
            ⚠️ CapeAI assistant temporarily unavailable
          </p>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ContextErrorBoundary;
