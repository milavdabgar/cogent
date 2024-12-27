"""add admin and management

Revision ID: 2024_12_27_add_admin
Revises: 4ba28fc7317e
Create Date: 2024-12-27 14:28:35.892766

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '2024_12_27_add_admin'
down_revision = '4ba28fc7317e'
branch_labels = None
depends_on = None

def upgrade():
    # Add admin role to UserRole enum
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('role',
                            existing_type=sa.Enum('principal', 'hod', 'faculty', 'lab_assistant', 'student',
                                                name='userrole'),
                            type_=sa.Enum('admin', 'principal', 'hod', 'faculty', 'lab_assistant', 'student',
                                        name='userrole'),
                            existing_nullable=True)
        batch_op.add_column(sa.Column('last_login', sa.Date(), nullable=True))

    # Create admin_details table
    op.create_table(
        'admin_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('super_admin', sa.Boolean(), nullable=True),
        sa.Column('date_of_joining', sa.Date(), nullable=True),
        sa.Column('access_level', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_details_id'), 'admin_details', ['id'], unique=False)

    # Create colleges table
    op.create_table(
        'colleges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('code', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('website', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_colleges_code'), 'colleges', ['code'], unique=True)
    op.create_index(op.f('ix_colleges_id'), 'colleges', ['id'], unique=False)
    op.create_index(op.f('ix_colleges_name'), 'colleges', ['name'], unique=False)

    # Create departments table
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('code', sa.String(), nullable=True),
        sa.Column('college_id', sa.Integer(), nullable=True),
        sa.Column('hod_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['college_id'], ['colleges.id'], ),
        sa.ForeignKeyConstraint(['hod_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_departments_id'), 'departments', ['id'], unique=False)
    op.create_index(op.f('ix_departments_name'), 'departments', ['name'], unique=False)

    # Create courses table
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('code', sa.String(), nullable=True),
        sa.Column('credits', sa.Integer(), nullable=True),
        sa.Column('type', sa.Enum('theory', 'practical', 'project', name='coursetype'), nullable=True),
        sa.Column('semester', sa.Integer(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_code'), 'courses', ['code'], unique=True)
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    op.create_index(op.f('ix_courses_name'), 'courses', ['name'], unique=False)

    # Create faculty_course_assignments table
    op.create_table(
        'faculty_course_assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('faculty_id', sa.Integer(), nullable=True),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('academic_year', sa.String(), nullable=True),
        sa.Column('semester', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.ForeignKeyConstraint(['faculty_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_faculty_course_assignments_id'), 'faculty_course_assignments', ['id'], unique=False)

def downgrade():
    # Drop tables in reverse order
    op.drop_index(op.f('ix_faculty_course_assignments_id'), table_name='faculty_course_assignments')
    op.drop_table('faculty_course_assignments')
    
    op.drop_index(op.f('ix_courses_name'), table_name='courses')
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_index(op.f('ix_courses_code'), table_name='courses')
    op.drop_table('courses')
    
    op.drop_index(op.f('ix_departments_name'), table_name='departments')
    op.drop_index(op.f('ix_departments_id'), table_name='departments')
    op.drop_table('departments')
    
    op.drop_index(op.f('ix_colleges_name'), table_name='colleges')
    op.drop_index(op.f('ix_colleges_id'), table_name='colleges')
    op.drop_index(op.f('ix_colleges_code'), table_name='colleges')
    op.drop_table('colleges')
    
    op.drop_index(op.f('ix_admin_details_id'), table_name='admin_details')
    op.drop_table('admin_details')
    
    # Revert UserRole enum changes
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('role',
                            existing_type=sa.Enum('admin', 'principal', 'hod', 'faculty', 'lab_assistant', 'student',
                                                name='userrole'),
                            type_=sa.Enum('principal', 'hod', 'faculty', 'lab_assistant', 'student',
                                        name='userrole'),
                            existing_nullable=True)
        batch_op.drop_column('last_login')
