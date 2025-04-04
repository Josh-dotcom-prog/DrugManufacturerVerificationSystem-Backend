"""other modals

Revision ID: 43e5a4de4b2b
Revises: e2071e2d7b3e
Create Date: 2025-04-04 15:05:23.011050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43e5a4de4b2b'
down_revision: Union[str, None] = 'e2071e2d7b3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manufacturers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('license_number', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('contact_email', sa.String(), nullable=False),
    sa.Column('contact_phone', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('license_file', sa.String(), nullable=True),
    sa.Column('certificate_file', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('license_number')
    )
    op.create_table('batches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('batch_number', sa.String(), nullable=False),
    sa.Column('manufacturer_id', sa.Integer(), nullable=True),
    sa.Column('manufacturing_date', sa.Date(), nullable=False),
    sa.Column('expiry_date', sa.Date(), nullable=False),
    sa.Column('status', sa.Enum('active', 'recalled', 'expired', name='batchstatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['manufacturer_id'], ['manufacturers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('batch_number')
    )
    op.create_table('drugs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('serial_number', sa.String(), nullable=False),
    sa.Column('batch_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('dosage', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('qr_code', sa.String(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('qr_code'),
    sa.UniqueConstraint('serial_number')
    )
    op.create_table('verifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('drug_id', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('device_info', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('is_authentic', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['drug_id'], ['drugs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verifications')
    op.drop_table('drugs')
    op.drop_table('batches')
    op.drop_table('manufacturers')
    # ### end Alembic commands ###
