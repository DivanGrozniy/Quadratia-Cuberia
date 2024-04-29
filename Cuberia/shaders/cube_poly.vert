#version 330 core

layout (location = 0) in vec3 in_vertex_pos;
layout (location = 1) in vec4 in_polygons_color;

out vec4 polygons_color;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main(){
	polygons_color = in_polygons_color;

	gl_Position = m_proj * m_view * m_model * vec4(in_vertex_pos, 1.0);
}

