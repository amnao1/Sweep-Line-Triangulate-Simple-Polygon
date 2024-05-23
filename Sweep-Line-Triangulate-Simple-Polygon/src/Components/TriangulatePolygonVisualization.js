import '../App.css';

import React, {useEffect, useRef, useState} from "react";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Card, Form, Spinner} from "react-bootstrap";
import Canvas from "./Canvas";


function TriangulatePoligonVisualization() {
    const [n, setN] = useState(null);
    const [polygons, setPolygons] = useState(null)
    const [triangles, setTriangles] = useState(null)
    const [isLoading, setIsLoading] = useState(false);

    const canvasRef = useRef(null);
    const contextRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        contextRef.current = context;
    }, []);

    function handleInputChange(event) {
        setN(event.target.value);
    }

    function crtajDijagonale(dijagonale){
        contextRef.current.beginPath();
        let n = dijagonale.length
        for (let i = 0; i < n-1; i+=2) {
            contextRef.current.moveTo(dijagonale[i][0], dijagonale[i][1])
            contextRef.current.lineTo(dijagonale[i+1][0], dijagonale[i+1][1]);
            console.log(dijagonale[i][0], dijagonale[i][1])
            console.log(dijagonale[i+1][0], dijagonale[i+1][1])
        }
        contextRef.current.closePath();
        contextRef.current.stroke();
    }
    function crtajPoligon(tacke, n){
        contextRef.current.beginPath();
        contextRef.current.moveTo(tacke[0][0], tacke[0][1]);
  
        for (let i = 1; i < n; i++) {
            contextRef.current.lineTo(tacke[i][0], tacke[i][1]);
        }
        contextRef.current.closePath();
        contextRef.current.lineWidth = 2
        contextRef.current.stroke();
    }

    function clearCanvas() {
        contextRef.current.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }
    function decompose(polygons){
        for (let index = 0; index < polygons.length; index++) {
            crtajPoligon(polygons[index], polygons[index].length)
            
        }
    }
    function triangulate(triangles){
        crtajDijagonale(triangles)
    }
    function getData(){
        setIsLoading(true); // set isLoading to true before making the API call

        const obj = { n: parseInt(n) };

        axios.post('/triangulate-polygon/', {...obj})
            .then((res) => {
                console.log('Done!');

                setN('');
                setIsLoading(false);
                clearCanvas();

                // draw
                const tacke = res.data.vrhovi
                const tackeP = res.data.vrhoviP
                const tackeD = res.data.vrhoviD
                setPolygons(tackeP)
                setTriangles(tackeD)
                crtajPoligon(tacke, tacke.length)
                
            }).catch((err) => {
            console.log(err);
        })
    }

    return (
        <div className="App">
            <div className="App-header">

                <h4 className="heading">Triagulation of Simple Polygon: Sweep Line Approach with <i>O(n log n)</i> Time Complexity</h4>

                <Form>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Control
                            type="number"
                            placeholder="Enter n"
                            onChange={handleInputChange}
                            value={n}
                            disabled={isLoading}
                        />
                        <Form.Text className="text-muted">
                            Algorithm will randomly generate <i>n</i> points and create simple polygon.
                        </Form.Text>
                    </Form.Group>
                    {isLoading ?
                        <Spinner
                            animation="border"
                            variant="light"
                        />
                        :
                        <div>
                            <Button
                                onClick={(e)=>{
                                    e.preventDefault();
                                    getData();
                                }}
                                type={"submit"}
                                disabled={!n}
                                style={{margin: 10}}>
                                Create polygon
                            </Button>
                            
                            <Button
                            onClick={(e)=>{
                                e.preventDefault();
                                decompose(polygons);
                            }}
                            type={"submit"}
                            disabled={!polygons}
                            style={{margin: 10}}>
                            Decompose polygon
                            </Button>
                            
                            <Button
                            onClick={(e)=>{
                                e.preventDefault();
                                triangulate(triangles);
                            }}
                            type={"submit"}
                            disabled={!triangles}
                            style={{margin: 10}}>
                            Triangulate polygon
                            </Button>
                        </div>
                    }
                </Form>

                <Canvas
                    width={1000}
                    height={550}
                    canvasRef={canvasRef}
                />
                <p
                    className="secondary-heading"
                    onClick={clearCanvas}>
                    Clear board
                </p>

            </div>
        </div>
    );
}

export default TriangulatePoligonVisualization;
