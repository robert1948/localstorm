import React from 'react';

const ImageTest = () => {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Image Loading Test</h2>
      <div>
        <h3>S3 Image:</h3>
        <img
          src="https://lightning-s3.s3.amazonaws.com/static/website/img/static/img/dashboard-preview.png"
          alt="Dashboard preview"
          style={{ maxWidth: '400px', border: '2px solid #ccc' }}
          onLoad={() => console.log('✅ S3 image loaded successfully')}
          onError={(e) => {
            console.error('❌ S3 image failed to load:', e.target.src);
            e.target.src = '/static/static/img/dashboard-preview.png';
            e.target.onerror = () => {
              console.error('❌ Fallback image also failed');
            };
          }}
        />
      </div>
      
      <div>
        <h3>Local Image:</h3>
        <img
          src="/static/static/img/dashboard-preview.png"
          alt="Dashboard preview local"
          style={{ maxWidth: '400px', border: '2px solid #ccc' }}
          onLoad={() => console.log('✅ Local image loaded successfully')}
          onError={() => console.error('❌ Local image failed to load')}
        />
      </div>
    </div>
  );
};

export default ImageTest;
