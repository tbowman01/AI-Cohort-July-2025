import React from 'react';

const LoadingSpinner = ({ 
  size = 'medium', 
  color = '#667eea', 
  text = '', 
  inline = false,
  overlay = false 
}) => {
  const sizes = {
    small: '20px',
    medium: '40px',
    large: '60px'
  };

  const spinnerStyles = {
    width: sizes[size],
    height: sizes[size],
    border: `3px solid rgba(0, 0, 0, 0.1)`,
    borderTop: `3px solid ${color}`,
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
    display: inline ? 'inline-block' : 'block',
    margin: inline ? '0' : '0 auto'
  };

  const containerStyles = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1rem',
    padding: '2rem',
    ...(overlay && {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      zIndex: 9999,
    })
  };

  const textStyles = {
    color: '#4a5568',
    fontSize: '0.9rem',
    fontWeight: '500',
    textAlign: 'center'
  };

  return (
    <>
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
      
      {overlay || !inline ? (
        <div style={containerStyles}>
          <div style={spinnerStyles} role="status" aria-label="Loading"></div>
          {text && <div style={textStyles} aria-live="polite">{text}</div>}
        </div>
      ) : (
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={spinnerStyles} role="status" aria-label="Loading"></div>
          {text && <span style={textStyles}>{text}</span>}
        </div>
      )}
    </>
  );
};

export default LoadingSpinner;