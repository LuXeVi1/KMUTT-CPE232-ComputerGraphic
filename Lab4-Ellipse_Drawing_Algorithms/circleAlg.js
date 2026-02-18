// Midpoint Circle Drawing Algorithm
function midpointCircle(cx, cy, r) {
    const points = [];
    
    // Round to integers
    cx = Math.round(cx);
    cy = Math.round(cy);
    r = Math.round(r);
    
    let x = 0;
    let y = r;
    let d = 1 - r;  // Initial decision parameter
    
    // Helper function to plot 8 symmetric points
    function plotSymmetricPoints(xc, yc, x, y) {
        points.push([xc + x, yc + y]);
        points.push([xc - x, yc + y]);
        points.push([xc + x, yc - y]);
        points.push([xc - x, yc - y]);
        points.push([xc + y, yc + x]);
        points.push([xc - y, yc + x]);
        points.push([xc + y, yc - x]);
        points.push([xc - y, yc - x]);
    }
    
    // Plot initial points
    plotSymmetricPoints(cx, cy, x, y);
    
    // Generate points for one octant, rest are symmetric
    while (x < y) {
        x++;
        
        if (d < 0) {
            // Midpoint is inside, move East
            d += 2 * x + 1;
        } else {
            // Midpoint is outside or on the circle, move Southeast
            y--;
            d += 2 * (x - y) + 1;
        }
        
        plotSymmetricPoints(cx, cy, x, y);
    }
    
    return points;
}