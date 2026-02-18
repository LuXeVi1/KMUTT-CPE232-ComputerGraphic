// Bresenham's Line Drawing Algorithm
function bresenhamLine(x0, y0, x1, y1) {
    const points = [];
    
    // Convert to integers
    x0 = Math.round(x0);
    y0 = Math.round(y0);
    x1 = Math.round(x1);
    y1 = Math.round(y1);
    
    const dx = Math.abs(x1 - x0);
    const dy = Math.abs(y1 - y0);
    const sx = x0 < x1 ? 1 : -1;  // Step direction in x
    const sy = y0 < y1 ? 1 : -1;  // Step direction in y
    let err = dx - dy;
    
    let x = x0;
    let y = y0;
    
    // Generate all points from (x0, y0) to (x1, y1)
    while (true) {
        points.push([x, y]);
        
        // If we've reached the endpoint, stop
        if (x === x1 && y === y1) break;
        
        const e2 = 2 * err;
        
        // Move in x direction
        if (e2 > -dy) {
            err -= dy;
            x += sx;
        }
        
        // Move in y direction
        if (e2 < dx) {
            err += dx;
            y += sy;
        }
    }
    
    return points;
}