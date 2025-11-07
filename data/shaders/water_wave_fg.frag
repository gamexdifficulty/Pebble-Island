#version 330

in vec2 uvs;
out vec4 FragColor;

uniform float uTime;

float amplitude = 0.035;
vec3 waterColor_1 = vec3(84.0/255, 128.0/255, 206.0/255);
vec3 waterColor_2 = vec3(88.0/255, 164.0/255, 220.0/255);

void main() {
    float wave_up_down = sin(uTime/2)*1.3;

    float wave1_1 = sin(uvs.x * 20 + (uTime/2) * 2);
    float wave1_2 = cos(uvs.x * 30 + (uTime/2) * 0.5);

    float wave2_1 = sin(uvs.x * 20 + ((uTime/2)+10) * 2);
    float wave2_2 = cos(uvs.x * 30 + ((uTime/2)+10) * 0.5);

    float combined_1 = (wave_up_down*2 + wave1_1 + wave1_2);
    float combined_2 = (wave_up_down*2 + wave2_1 + wave2_2);

    float waveY_1 = 0.25 + combined_1 * amplitude;
    float waveY_2 = 0.45 + combined_2 * amplitude;

    if (uvs.y > waveY_1) {
        if (uvs.y > waveY_2) {
            FragColor = vec4(waterColor_2, 1.0);
        }
        else {
            FragColor = vec4(waterColor_1, 1.0);
        }
    } else {
        FragColor = vec4(0.0, 0.0, 0.0, 0.0);
    }
}
