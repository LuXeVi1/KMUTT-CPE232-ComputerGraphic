function midpointEllipse(xc, yc, rx, ry) {
    const points = [];

    // Round to integers to align with the pixel grid
    xc = Math.round(xc);
    yc = Math.round(yc);
    rx = Math.round(rx);
    ry = Math.round(ry);

    let x = 0;
    let y = ry;

    // Initial decision parameter for Region 1
    let d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx);
    let dx = 2 * ry * ry * x;
    let dy = 2 * rx * rx * y;

    // Region 1: slope < 1
    while (dx < dy) {
        // Plot points in all 4 quadrants
        points.push([xc + x, yc + y]);
        points.push([xc - x, yc + y]);
        points.push([xc + x, yc - y]);
        points.push([xc - x, yc - y]);

        if (d1 < 0) {
            x++;
            dx += 2 * ry * ry;
            d1 += dx + (ry * ry);
        } else {
            x++;
            y--;
            dx += 2 * ry * ry;
            dy -= 2 * rx * rx;
            d1 += dx - dy + (ry * ry);
        }
    }

    // Decision parameter for Region 2
    let d2 = ((ry * ry) * ((x + 0.5) * (x + 0.5))) +
        ((rx * rx) * ((y - 1) * (y - 1))) -
        (rx * rx * ry * ry);

    // Region 2: slope >= 1
    while (y >= 0) {
        points.push([xc + x, yc + y]);
        points.push([xc - x, yc + y]);
        points.push([xc + x, yc - y]);
        points.push([xc - x, yc - y]);

        if (d2 > 0) {
            y--;
            dy -= 2 * rx * rx;
            d2 += (rx * rx) - dy;
        } else {
            y--;
            x++;
            dx += 2 * ry * ry;
            dy -= 2 * rx * rx;
            d2 += dx - dy + (rx * rx);
        }
    }

    return points;
}

// Fast Ellipse Algorithm (John Kennedy) - Integer Only
function fastEllipse(xc, yc, rx, ry) {
    const points = [];

    xc = Math.round(xc);
    yc = Math.round(yc);
    rx = Math.round(rx);
    ry = Math.round(ry);

    let x = 0;
    let y = ry;

    const dxInit = 2 * ry * ry;
    const dyInit = 2 * rx * rx;
    let dx = 0; // 2 * ry^2 * x (x=0)
    let dy = dyInit * y; // 2 * rx^2 * y

    // Initial decision parameter Region 1
    // D1 = 4 * d1_init
    // d1_init = ry^2 - rx^2*ry + 0.25*rx^2
    // D1 = 4*ry^2 - 4*rx^2*ry + rx^2
    let D1 = (4 * ry * ry) - (4 * rx * rx * ry) + (rx * rx);

    while (dx < dy) {
        // Plot points
        points.push([xc + x, yc + y]);
        points.push([xc - x, yc + y]);
        points.push([xc + x, yc - y]);
        points.push([xc - x, yc - y]);

        if (D1 < 0) {
            x++;
            dx += dxInit;
            // D1 += 4*dx + 4*ry^2 (based on new dx, it's 2*ry^2*2*x... wait)
            // Original: d1 += 2*ry^2*x (new x) + ry^2
            // 4*d1 += 8*ry^2*x + 4*ry^2
            // dx (new) = 2*ry^2*x
            // So 4*dx = 8*ry^2*x.
            // D1 += 4*dx + 2*dxInit (2*2*ry^2 = 4*ry^2). Correct.
            D1 += (4 * dx) + (2 * dxInit);
        } else {
            x++;
            y--;
            dx += dxInit;
            dy -= dyInit;
            // Original: d1 += 2*ry^2*x (new) - 2*rx^2*y (new) + ry^2
            // 4*d1 += 8*ry^2*x - 8*rx^2*y + 4*ry^2
            // 4*dx = 8*ry^2*x.
            // 4*dy = 8*rx^2*y.
            // D1 += 4*dx - 4*dy + 2*dxInit. Correct.
            D1 += (4 * dx) - (4 * dy) + (2 * dxInit);
        }
    }

    // Region 2
    // D2 = 4 * d2_init
    // Using current x, y (last of region 1 loop)
    // d2_init = ry^2(x+0.5)^2 + rx^2(y-1)^2 - rx^2*ry^2
    // D2 = ry^2(2x+1)^2 + 4*rx^2(y-1)^2 - 4*rx^2*ry^2
    let D2 = (ry * ry * ((2 * x + 1) * (2 * x + 1))) +
        (4 * rx * rx * ((y - 1) * (y - 1))) -
        (4 * rx * rx * ry * ry);

    while (y >= 0) {
        points.push([xc + x, yc + y]);
        points.push([xc - x, yc + y]);
        points.push([xc + x, yc - y]);
        points.push([xc - x, yc - y]);

        if (D2 > 0) {
            y--;
            dy -= dyInit;
            // Original: d2 += rx^2 - 2*rx^2*y (new)
            // 4*d2 += 4*rx^2 - 8*rx^2*y (new)
            // 4*dy = 8*rx^2*y (new)
            // D2 += 4*rx^2 - 4*dy.
            // 2*dyInit = 4*rx^2. Correct.
            D2 += (2 * dyInit) - (4 * dy);
        } else {
            y--;
            x++;
            dx += dxInit;
            dy -= dyInit;
            // Original: d2 += 2*ry^2*x (new) - 2*rx^2*y (new) + rx^2
            // 4*d2 += 8*ry^2*x - 8*rx^2*y + 4*rx^2
            // D2 += 4*dx - 4*dy + 2*dyInit. Correct.
            D2 += (4 * dx) - (4 * dy) + (2 * dyInit);
        }
    }

    return points;
}
