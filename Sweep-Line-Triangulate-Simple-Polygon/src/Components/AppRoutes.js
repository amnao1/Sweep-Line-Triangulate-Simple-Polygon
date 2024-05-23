import React from 'react';
import {Route, Routes} from 'react-router-dom';
import TriangulatePoligonVisualization from './TriangulatePolygonVisualization.js';

const AppRoutes = () => {
    return (
        <Routes>

            <Route index path="/" element={<TriangulatePoligonVisualization />} />
            <Route exact path="/triangulate-polygon" element={<TriangulatePoligonVisualization />} />
        
        </Routes>
    );
};

export default AppRoutes;
