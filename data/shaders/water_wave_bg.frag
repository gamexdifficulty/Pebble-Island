#version 330

in vec2 uvs;
out vec4 FragColor;

uniform float uTime;

float amplitude = 0.035;
vec3 waterColor = vec3(77.0/255, 101.0/255, 180.0/255);

void main() {
    float wave_up_down = sin((uTime+10)/2);

    float wave1 = sin(uvs.x * 15 + ((uTime/2)+20) * 2);
    float wave2 = cos(uvs.x * 25 + ((uTime/2)+20) * 0.5);

    float combined = (wave_up_down + wave1 + wave2);
    float waveY = 0.35 + combined * amplitude;

    if (uvs.y > waveY) {
        FragColor = vec4(waterColor, 1.0);
    } else {
        FragColor = vec4(0.0, 0.0, 0.0, 0.0);
    }
}
