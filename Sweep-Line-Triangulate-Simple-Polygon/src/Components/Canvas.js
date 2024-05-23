import React from 'react';

const Canvas = ({width, height, canvasRef}) => {

    return (
        <canvas
            ref={canvasRef}
            width={width}
            height={height}
            style={canvasRefStyle}
        />
    );

};

export default Canvas;

const canvasRefStyle = {
    // border:'solid white 1px',
    backgroundColor: '#ffffff',
    boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
    marginTop: '50px'
};
