#version 330

in vec3 position;
in vec3 normal;

out vec4 f_color;

uniform vec3 color;
uniform vec3 light_color;
uniform vec3 view_position;
uniform vec3 light_position;

void main()
{
    float ambient_strength = 0.3;
    float diffuse_strength = 0.7;
    float specular_strength = 0.5;
    float shininess = 1.0;

    vec3 ambient = ambient_strength * light_color;

    vec3 light_direction = normalize(light_position - position);
    vec3 diffuse = diffuse_strength * max(dot(normal, light_direction), 0.0) * light_color;

    vec3 view_direction = normalize(view_position - position);
    vec3 reflection_direction = reflect(-light_direction, normal);
    vec3 specular = specular_strength * pow(max(dot(view_direction, reflection_direction), 0.0), shininess) * light_color;

    vec3 phong_shading = color * (ambient + diffuse + specular);

    f_color = vec4(phong_shading, 1.0);
}
