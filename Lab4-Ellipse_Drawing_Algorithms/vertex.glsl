// vertex.glsl – Vertex shader for plotting points
attribute vec2 a_position;   // input position (in clip space coordinates)
void main() {
    float x_ndc = (a_position.x / 511.0) * 2.0 - 1.0;
    float y_ndc = (a_position.y / 511.0) * 2.0 - 1.0;
    gl_Position = vec4(a_position, 0.0, 1.0);
    gl_PointSize = 2.0;      // size of each point (in pixels)
}
