// client/src/api/auth.js

const API_BASE = process.env.NODE_ENV === 'production' 
  ? 'https://www.cape-control.com/api' 
  : 'http://localhost:8001';

export async function loginUser(email, password) {
  const response = await fetch(`${API_BASE}/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      username: email,
      password: password
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }

  return await response.json(); // { access_token, token_type }
}

// V2 Registration API Methods

/**
 * Validate email availability for registration
 */
export async function validateEmail(email) {
  try {
    const response = await fetch(`${API_BASE}/auth/v2/validate-email?email=${encodeURIComponent(email)}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    // Check if response is JSON
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error('Server returned non-JSON response');
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || error.message || 'Email validation failed');
    }

    return await response.json(); // { available: bool, reason?: string, message: string }
  } catch (error) {
    console.error('Email validation error:', error);
    return { 
      available: null, 
      reason: 'validation_error',
      message: 'Unable to validate email. Please try again.'
    };
  }
}

/**
 * Validate password strength
 */
export async function validatePassword(password) {
  try {
    const response = await fetch(`${API_BASE}/auth/v2/validate-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password })
    });

    // Check if response is JSON
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error('Server returned non-JSON response');
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || error.message || 'Password validation failed');
    }

    return await response.json(); // { valid: bool, score: int, requirements: object }
  } catch (error) {
    console.error('Password validation error:', error);
    return {
      valid: false,
      score: 0,
      requirements: {
        minLength: false,
        hasUpper: false,
        hasLower: false,
        hasNumber: false,
        hasSpecial: false
      }
    };
  }
}

/**
 * Register new user with V2 enhanced validation
 */
export async function registerUserV2(userData) {
  try {
    const response = await fetch(`${API_BASE}/auth/v2/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });

    // Check if response is JSON
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      console.error('Non-JSON response received:', await response.text());
      throw new Error('Server error: Invalid response format');
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || data.message || 'Registration failed');
    }

    return data; // { id, email, access_token?, ... }
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
}

/**
 * Enhanced login with better error handling
 */
export async function loginUserV2(email, password) {
  try {
    const response = await fetch(`${API_BASE}/auth/v2/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    return await response.json(); // { access_token, token_type, user: {...} }
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}
