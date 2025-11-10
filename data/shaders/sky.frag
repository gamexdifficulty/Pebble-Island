#version 330

in vec2 uvs;

uniform vec4 color1;
uniform vec4 color2;

out vec4 FragColor;

void main() {
    float diff_r = (color2.r-color1.r)*uvs.y;
    float diff_g = (color2.g-color1.g)*uvs.y;
    float diff_b = (color2.b-color1.b)*uvs.y;

    vec4 color = vec4((color1.r+diff_r)/255.0,(color1.g+diff_g)/255.0,(color1.b+diff_b)/255.0,1.0);
    
    FragColor = color;
}