"""add models

Revision ID: 9be1af8bfbbd
Revises: 839b6649adf9
Create Date: 2024-10-26 18:01:45.676007

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '9be1af8bfbbd'
down_revision = '839b6649adf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charityproject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_amount', sa.Integer(), nullable=True),
    sa.Column('invested_amount', sa.Integer(), nullable=True),
    sa.Column('fully_invested', sa.Boolean(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_charityproject_id'), ['id'], unique=False)

    op.create_table('donation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_amount', sa.Integer(), nullable=True),
    sa.Column('invested_amount', sa.Integer(), nullable=True),
    sa.Column('fully_invested', sa.Boolean(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_donation_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_donation_id'))

    op.drop_table('donation')
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_charityproject_id'))

    op.drop_table('charityproject')
    # ### end Alembic commands ###
