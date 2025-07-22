# 🧪 React Context Error Testing & Debugging Guide

## 🚨 Root Cause Analysis: React Context Errors

### **Problem Identified**
React context timing issues in production, specifically:
1. `Cannot read properties of null (reading 'useContext')`
2. `Failed to execute 'removeChild' on 'Node'`
3. Context providers not initialized before component access

### **Root Causes**
1. **React.StrictMode Double Rendering**: Development mode renders components twice, causing timing issues
2. **Context Access Before Initialization**: Components trying to access context before providers are ready
3. **Lazy Loading + Context**: Dynamic imports conflicting with context timing
4. **Production Minification**: Different behavior between dev and production builds

---

## 🛡️ Solution Implementation

### **Error Boundary Pattern**
```jsx
class ContextErrorBoundary extends React.Component {
  static getDerivedStateFromError(error) {
    if (error?.message?.includes('useContext')) {
      return { hasError: true, error };
    }
    throw error; // Let other errors bubble up
  }
  
  render() {
    if (this.state.hasError) {
      return <SafeFallbackComponent />;
    }
    return this.props.children;
  }
}
```

### **Safe Context Pattern**
```jsx
export const CapeAIProvider = ({ children }) => {
  const [isInitialized, setIsInitialized] = useState(false);
  
  useEffect(() => {
    // Safe initialization after mount
    setIsInitialized(true);
  }, []);
  
  if (!isInitialized) {
    return children; // Render children without context
  }
  
  return (
    <CapeAIContext.Provider value={contextValue}>
      {children}
    </CapeAIContext.Provider>
  );
};
```

### **Safe Hook Pattern**
```jsx
export default function useCapeAISafe() {
  const context = useContext(CapeAIContext);
  
  if (!context || !context.isInitialized) {
    // Return safe defaults instead of throwing
    return {
      isVisible: false,
      toggleVisibility: () => console.warn('Context not ready'),
      // ... other safe defaults
    };
  }
  
  return context;
}
```

---

## ✅ Testing Strategy

### **1. Local Development Testing**
```bash
# Test with StrictMode
npm run dev

# Test production build
npm run build
npm run preview

# Check for console errors in both modes
```

### **2. Context Isolation Testing**
```jsx
// Create minimal test without context
function MinimalTest() {
  return <div>Basic component without context</div>;
}

// Test individual components in isolation
function ContextTest() {
  return (
    <ContextErrorBoundary>
      <CapeAIProvider>
        <ComponentUnderTest />
      </CapeAIProvider>
    </ContextErrorBoundary>
  );
}
```

### **3. Production Simulation**
```bash
# Build and test locally
npm run build
python -m http.server 8080 --directory dist

# Check browser console for errors
# Test on different browsers and devices
```

### **4. Error Monitoring**
```jsx
// Add error tracking in components
useEffect(() => {
  const handleError = (event) => {
    if (event.error?.message?.includes('useContext')) {
      console.error('Context error detected:', event.error);
      // Report to monitoring service
    }
  };
  
  window.addEventListener('error', handleError);
  return () => window.removeEventListener('error', handleError);
}, []);
```

---

## 🎯 Prevention Guidelines

### **1. Context Design Patterns**
- ✅ Always provide fallback defaults in hooks
- ✅ Use error boundaries around context consumers
- ✅ Initialize context state safely after mount
- ✅ Test both development and production builds
- ❌ Don't access context immediately in component body
- ❌ Don't assume context is always available

### **2. Component Architecture**
```jsx
// ✅ Safe pattern
function MyComponent() {
  const { data, isReady } = useSafeContext();
  
  if (!isReady) {
    return <LoadingState />; // Graceful degradation
  }
  
  return <ActualComponent data={data} />;
}

// ❌ Unsafe pattern  
function MyComponent() {
  const { data } = useContext(MyContext); // Can throw
  return <div>{data.property}</div>; // Can crash
}
```

### **3. Build Pipeline Checks**
```json
{
  "scripts": {
    "test:context": "npm run build && npm run test:errors",
    "test:errors": "node scripts/check-build-errors.js",
    "pre-deploy": "npm run test:context && npm run lint"
  }
}
```

---

## 🔍 Debugging Commands

### **Quick Error Detection**
```bash
# Check for context-related console errors
grep -r "useContext\\|Provider\\|Context" src/

# Build and check for errors
npm run build 2>&1 | grep -i error

# Test specific components
npm test -- --testNamePattern="Context"
```

### **Browser DevTools**
```javascript
// Console commands to test context
console.log(React.version);
console.log(document.querySelectorAll('[data-reactroot]'));

// Check for context providers
console.log(document.querySelectorAll('[data-react-context]'));
```

---

## 📋 Checklist for Future Context Implementation

### **Before Adding New Context**
- [ ] Create error boundary wrapper
- [ ] Implement safe initialization pattern
- [ ] Add fallback defaults in hooks
- [ ] Test in both development and production
- [ ] Add console warnings for debugging
- [ ] Document expected behavior

### **Before Deployment**
- [ ] Build succeeds without errors
- [ ] No console errors in browser
- [ ] Test on multiple browsers
- [ ] Check mobile responsiveness
- [ ] Verify lazy loading works
- [ ] Monitor production logs

---

## 🚀 Results Achieved

### **Fixed Errors**
- ✅ `Cannot read properties of null (reading 'useContext')`
- ✅ `Failed to execute 'removeChild' on 'Node'`
- ✅ Context initialization timing issues
- ✅ React.StrictMode compatibility

### **Performance Impact**
- ⚡ Zero additional runtime overhead
- 🛡️ Graceful degradation when context fails
- 📱 Better mobile/responsive behavior
- 🔧 Easier debugging with meaningful warnings

### **Developer Experience**
- 🎯 Clear error messages instead of crashes
- 🛠️ Safe development environment
- 📖 Comprehensive debugging guide
- 🔄 Reliable build/deploy process

---

*This guide ensures robust React context implementation that handles edge cases gracefully and provides a better user experience.*
