#version 330

in vec3 in_position;
in vec3 in_normal;

out vec3 FragPos;
out vec3 Normal;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main() {
    FragPos = vec3(model * vec4(in_position, 1.0));
    Normal = mat3(transpose(inverse(model))) * in_normal;  
    gl_Position = projection * view * vec4(FragPos, 1.0);
}