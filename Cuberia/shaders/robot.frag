#version 330 core

layout (location = 0) out vec4 fragment_color;

in vec3 polygons_color;

void main(){
	fragment_color = vec4(polygons_color, 1.0);
}
