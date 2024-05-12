#version 330

in vec3 in_position;
in vec3 in_normal;

out vec3 position;
out vec3 normal;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main() {
    position = in_position;
    normal = normalize(in_normal);
    gl_Position = projection * view * model * vec4(in_position, 1.0);
}