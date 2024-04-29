#version 330 core

layout (location = 0) out vec4 fragment_color;

in vec3 lines_color;

void main(){
	fragment_color = vec4(lines_color, 1.0);
}
