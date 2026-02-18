window.onload = () => {
    main();
};

const shapes = []

async function main() {
    const canvas = document.getElementById('glCanvas');
    const gl = canvas.getContext('webgl');
    if (!gl) {
        alert("Unable to initialize WebGL.");
        return;
    }

    // Configure the WebGL viewport and clear the canvas
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(1.0, 1.0, 1.0, 1.0);  // white background
    gl.clear(gl.COLOR_BUFFER_BIT);

    // Load shader source code from files
    const [vsSource, fsSource] = await Promise.all([
        fetch('shaders/vertex.glsl').then(res => res.text()),
        fetch('shaders/fragment.glsl').then(res => res.text())
    ]);

    // Compile the vertex and fragment shaders
    const vertexShader = compileShader(gl, vsSource, gl.VERTEX_SHADER);
    const fragmentShader = compileShader(gl, fsSource, gl.FRAGMENT_SHADER);
    // Link shaders into a program
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error("Program link error:", gl.getProgramInfoLog(program));
        return;
    }
    gl.useProgram(program);

    const positions = [];

    // Locate the position attribute in the shader and enable it
    const posAttrLoc = gl.getAttribLocation(program, 'a_position');
    gl.enableVertexAttribArray(posAttrLoc);

    // Create a buffer to hold point positions
    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    // Describe the layout of the buffer data for the shader (2 floats per attribute instance)
    gl.vertexAttribPointer(posAttrLoc, 2, gl.FLOAT, false, 0, 0);

    // Variables to track the first click (start point)
    let startPoint = null;

    // Helper function to convert pixel coordinates to NDC (Normalized Device Coordinates)
    function pixelToNDC(pixelX, pixelY) {
        // WebGL uses NDC from -1 to 1
        // Convert pixel (0 to width/height) to NDC (-1 to 1)
        const ndcX = (pixelX / canvas.width) * 2 - 1;
        const ndcY = (pixelY / canvas.height) * 2 - 1;
        return [ndcX, ndcY];
    }

    // Set up event listener for canvas clicks to get line endpoints
    canvas.addEventListener('click', function (event) {
        // Get mouse coordinates relative to the canvas
        const canvasX = event.offsetX;
        const canvasY = event.offsetY;
        // Convert canvas Y (top-left origin) to pixel grid Y (bottom-left origin)
        const pixelX = canvasX;
        const pixelY = canvas.height - 1 - canvasY;  // invert Y axis

        // Get the selected drawing mode (line or circle)
        const drawMode = document.querySelector('input[name="mode"]:checked').value;

        if (startPoint === null) {
            // First click: record the starting point
            startPoint = { x: pixelX, y: pixelY };
        } else {
            // Second click: we have an end point, so draw the shape
            const endPoint = { x: pixelX, y: pixelY };
            let shapePixels = [];

            if (drawMode === 'line') {
                // Use Bresenham's algorithm to get all points on the line
                shapePixels = bresenhamLine(startPoint.x, startPoint.y, endPoint.x, endPoint.y);
            } else if (drawMode === 'circle') {
                // Calculate radius from center to click point
                const radius = Math.sqrt(
                    Math.pow(endPoint.x - startPoint.x, 2) +
                    Math.pow(endPoint.y - startPoint.y, 2)
                );
                // Use Midpoint Circle algorithm to get all points on the circle
                shapePixels = midpointCircle(startPoint.x, startPoint.y, radius);
            } else if (drawMode === 'ellipse_midpoint') {
                const rx = Math.abs(endPoint.x - startPoint.x);
                const ry = Math.abs(endPoint.y - startPoint.y);
                shapePixels = midpointEllipse(startPoint.x, startPoint.y, rx, ry);
            } else if (drawMode === 'ellipse_fast') {
                const rx = Math.abs(endPoint.x - startPoint.x);
                const ry = Math.abs(endPoint.y - startPoint.y);
                shapePixels = fastEllipse(startPoint.x, startPoint.y, rx, ry);
            }

            // Convert pixel coordinates to NDC for WebGL

            const positions = []
            for (const [x, y] of shapePixels) {
                const [ndcX, ndcY] = pixelToNDC(x, y);
                positions.push(ndcX, ndcY);
            }

            shapes.push({
                positions: new Float32Array(positions),
                count: shapePixels.length,
            })

            for (const s of shapes) {
                gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
                gl.bufferData(gl.ARRAY_BUFFER, s.positions, gl.STATIC_DRAW);

                // Draw the points as a series of GL_POINTS
                gl.drawArrays(gl.POINTS, 0, s.count);
            }
            // Reset startPoint so we can draw another shape
            startPoint = null;
        }
    });
}

// Helper function to compile a shader from source
function compileShader(gl, source, shaderType) {
    const shader = gl.createShader(shaderType);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error("Shader compile error:", gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }
    return shader;
}
