// gl-matrix.js – Manual implementation of 4x4 matrix operations (column-major order)
function matIdentity() {
    // Returns a new identity matrix (4x4)
    return new Float32Array([
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1
    ]);
}

function matMultiply(a, b) {
    // Multiplies two 4x4 matrices (column-major): result = a * b
    const out = new Float32Array(16);
    for (let col = 0; col < 4; col++) {
        for (let row = 0; row < 4; row++) {
            out[col * 4 + row] =
                a[0 * 4 + row] * b[col * 4 + 0] +
                a[1 * 4 + row] * b[col * 4 + 1] +
                a[2 * 4 + row] * b[col * 4 + 2] +
                a[3 * 4 + row] * b[col * 4 + 3];
        }
    }
    return out;
}

function matTranslate(tx, ty, tz) {
    // Returns a 4x4 translation matrix (column-major)
    return new Float32Array([
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        tx, ty, tz, 1
    ]);
}

function matScale(sx, sy, sz) {
    // Returns a 4x4 scaling matrix (column-major)
    return new Float32Array([
        sx, 0, 0, 0,
        0, sy, 0, 0,
        0, 0, sz, 0,
        0, 0, 0, 1
    ]);
}

function matRotateX(angleRad) {
    // Returns a 4x4 rotation matrix around the X-axis (column-major)
    const c = Math.cos(angleRad);
    const s = Math.sin(angleRad);
    return new Float32Array([
        1, 0, 0, 0,
        0, c, s, 0,
        0, -s, c, 0,
        0, 0, 0, 1
    ]);
}

function matRotateY(angleRad) {
    // Returns a 4x4 rotation matrix around the Y-axis (column-major)
    const c = Math.cos(angleRad);
    const s = Math.sin(angleRad);
    return new Float32Array([
        c, 0, -s, 0,
        0, 1, 0, 0,
        s, 0, c, 0,
        0, 0, 0, 1
    ]);
}

function matRotateZ(angleRad) {
    // Returns a 4x4 rotation matrix around the Z-axis (column-major)
    const c = Math.cos(angleRad);
    const s = Math.sin(angleRad);
    return new Float32Array([
        c, s, 0, 0,
        -s, c, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1
    ]);
}

function matPerspective(fovDeg, aspect, near, far) {
    // Creates a perspective projection matrix with given field-of-view (degrees), aspect ratio, near and far planes
    const fovRad = fovDeg * Math.PI / 180.0;
    const f = 1.0 / Math.tan(fovRad / 2.0);   // focal length (cotangent of half FOV)
    const nf = 1.0 / (near - far);           // reciprocal of (near - far)
    const out = new Float32Array(16);
    out[0] = f / aspect;
    out[1] = 0;
    out[2] = 0;
    out[3] = 0;
    out[4] = 0;
    out[5] = f;
    out[6] = 0;
    out[7] = 0;
    out[8] = 0;
    out[9] = 0;
    out[10] = (far + near) * nf;
    out[11] = -1;
    out[12] = 0;
    out[13] = 0;
    out[14] = (2 * far * near) * nf;
    out[15] = 0;
    return out;
}