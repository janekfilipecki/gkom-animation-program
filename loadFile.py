from OpenGL.GL import (glBegin, glEnd, glVertex3fv, GL_TRIANGLES)


def load_obj(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = list(map(float, line.split()[1:]))
                vertices.append(vertex)
            elif line.startswith('f '):
                face = [int(idx.split('/')[0]) - 1 for idx in line.split()[1:]]
                faces.append(face)
    return vertices, faces


def draw_model(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
