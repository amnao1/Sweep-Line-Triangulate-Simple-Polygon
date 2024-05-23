import './App.css';
import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Nav, Navbar} from "react-bootstrap";
import Container from "react-bootstrap/Container";
import TriangulatePoligonVisualization from './Components/TriangulatePolygonVisualization';
import AppRoutes from "./Components/AppRoutes";
import {Link} from "react-router-dom";


function App() {

    return (
        <div className="App">
            <Navbar bg="dark" variant="dark">
                <Container>
                        <Navbar.Brand href="#home">Kompjutaciona geometrija</Navbar.Brand>
                    <Nav className="me-auto">
                        <Nav.Link as={Link} to='/triangulate-polygon'> Sweep Line algorithm </Nav.Link>
                    </Nav>
                </Container>
            </Navbar>
            <AppRoutes />
        </div>
    );
}

export default App;
