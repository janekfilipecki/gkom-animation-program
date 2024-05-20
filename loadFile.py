from OpenGL.GL import (glBegin, glEnd, glVertex3fv, GL_TRIANGLES,
                       glNormal3fv)
import math


def draw_model(vertices, faces, normals):
    """Draw the loaded model."""
    glBegin(GL_TRIANGLES)
    for i, face in enumerate(faces):
        normal = normals[i]
        for vertex_index in face:
            glNormal3fv(normal)
            glVertex3fv(vertices[vertex_index])
    glEnd()


def load_obj(file_path):
    """Loads an OBJ file and returns vertices, faces, and normals."""
    vertices = []
    faces = []
    normals = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vn '):
                normals.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('f '):
                face = [int(part.split('//')[0]) -
                        1 for part in line.strip().split()[1:]]
                faces.append(face)
    if not normals:
        normals = calculate_normals(vertices, faces)
    return vertices, faces, normals


def calculate_normals(vertices, faces):
    """Calculates normals for each face in the model."""
    normals = []
    for face in faces:
        v1 = vertices[face[0]]
        v2 = vertices[face[1]]
        v3 = vertices[face[2]]
        normal = compute_normal(v1, v2, v3)
        normals.append(normal)
    return normals


def compute_normal(v1, v2, v3):
    """Computes the normal vector of a triangle given its vertices."""
    # Calculate the vectors from v1 to v2 and v1 to v3
    vector1 = [v2[i] - v1[i] for i in range(3)]
    vector2 = [v3[i] - v1[i] for i in range(3)]

    # Compute the cross product of the vectors
    cross_product = [
        vector1[1] * vector2[2] - vector1[2] * vector2[1],
        vector1[2] * vector2[0] - vector1[0] * vector2[2],
        vector1[0] * vector2[1] - vector1[1] * vector2[0]
    ]

    # Normalize the cross product to get the normal vector
    length = math.sqrt(sum([cross_product[i] ** 2 for i in range(3)]))
    normal = [cross_product[i] / length for i in range(3)]

    return normal
