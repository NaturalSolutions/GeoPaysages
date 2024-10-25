"""translations

Revision ID: d7fd422e1054
Revises: 4a02bd35bb30
Create Date: 2024-10-22 12:20:06.196024

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d7fd422e1054"
down_revision = "4a02bd35bb30"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "lang",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("label", sa.String(), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=True, default=False),
        sa.PrimaryKeyConstraint("id"),
        schema="geopaysages",
    )
    op.create_index(
        "unique_is_default_true",
        "lang",
        ["is_default"],
        unique=True,
        postgresql_where=sa.text("is_default IS TRUE"),
        schema="geopaysages",
    )
    # Insert default lang 'fr'
    op.execute(
        sa.text(
            """
        INSERT INTO geopaysages.lang (id, label, is_published, is_default)
        VALUES ('fr', 'Français', true, true)
    """
        )
    )

    op.create_table(
        "communes_translation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nom_commune", sa.String(), nullable=True),
        sa.Column("row_id", sa.String(), nullable=True),
        sa.Column("lang_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["lang_id"], ["geopaysages.lang.id"], name="communes_translation_fk_lang"
        ),
        sa.ForeignKeyConstraint(
            ["row_id"],
            ["geopaysages.communes.code_commune"],
            name="commune_code_commune",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="geopaysages",
    )
    # Insert existing communes in translation table
    op.execute(
        sa.text(
            """
        INSERT INTO geopaysages.communes_translation (nom_commune, row_id, lang_id)
        SELECT nom_commune, code_commune, 'fr'
        FROM geopaysages.communes
    """
        )
    )

    op.create_table(
        "dico_stheme_translation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name_stheme", sa.String(), nullable=True),
        sa.Column("row_id", sa.Integer(), nullable=True),
        sa.Column("lang_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["lang_id"], ["geopaysages.lang.id"], name="dico_stheme_translation_fk_lang"
        ),
        sa.ForeignKeyConstraint(
            ["row_id"], ["geopaysages.dico_stheme.id_stheme"], name="stheme_id_stheme"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="geopaysages",
    )
    op.execute(
        sa.text(
            """
        INSERT INTO geopaysages.dico_stheme_translation (name_stheme, row_id, lang_id)
        SELECT name_stheme, id_stheme, 'fr'
        FROM geopaysages.dico_stheme
    """
        )
    )

    op.create_table(
        "dico_theme_translation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name_theme", sa.String(), nullable=True),
        sa.Column("row_id", sa.Integer(), nullable=True),
        sa.Column("lang_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["lang_id"], ["geopaysages.lang.id"], name="dico_theme_translation_fk_lang"
        ),
        sa.ForeignKeyConstraint(
            ["row_id"], ["geopaysages.dico_theme.id_theme"], name="theme_id_theme"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="geopaysages",
    )
    op.execute(
        sa.text(
            """
        INSERT INTO geopaysages.dico_theme_translation (name_theme, row_id, lang_id)
        SELECT name_theme, id_theme, 'fr'
        FROM geopaysages.dico_theme
    """
        )
    )

    op.create_table(
        "t_observatory_translation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=True),
        sa.Column("row_id", sa.Integer(), nullable=True),
        sa.Column("lang_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["lang_id"],
            ["geopaysages.lang.id"],
            name="t_observatory_translation_fk_lang",
        ),
        sa.ForeignKeyConstraint(
            ["row_id"], ["geopaysages.t_observatory.id"], name="observatory_id"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="geopaysages",
    )
    op.execute(
        sa.text(
            """
        INSERT INTO geopaysages.t_observatory_translation (title, is_published, row_id, lang_id)
        SELECT title, is_published, id, 'fr'
        FROM geopaysages.t_observatory
    """
        )
    )

    op.create_table(
        "t_site_translation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name_site", sa.String(), nullable=True),
        sa.Column("desc_site", sa.String(), nullable=True),
        sa.Column("testim_site", sa.String(), nullable=True),
        sa.Column("legend_site", sa.String(), nullable=True),
        sa.Column("publish_site", sa.Boolean(), nullable=True),
        sa.Column("row_id", sa.Integer(), nullable=True),
        sa.Column("lang_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["lang_id"], ["geopaysages.lang.id"], name="t_site_translation_fk_lang"
        ),
        sa.ForeignKeyConstraint(
            ["row_id"], ["geopaysages.t_site.id_site"], name="site_id_site"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="geopaysages",
    )
    op.execute(
        sa.text(
            """
        INSERT INTO geopaysages.t_site_translation (name_site, desc_site, testim_site, legend_site, publish_site, row_id, lang_id)
        SELECT name_site, desc_site, testim_site, legend_site, publish_site, id_site, 'fr'
        FROM geopaysages.t_site
    """
        )
    )

    op.drop_column("communes", "nom_commune", schema="geopaysages")
    op.drop_column("dico_stheme", "name_stheme", schema="geopaysages")
    op.drop_column("dico_theme", "name_theme", schema="geopaysages")
    op.drop_column("t_observatory", "title", schema="geopaysages")
    op.drop_column("t_observatory", "is_published", schema="geopaysages")
    op.drop_column("t_site", "publish_site", schema="geopaysages")
    op.drop_column("t_site", "name_site", schema="geopaysages")
    op.drop_column("t_site", "desc_site", schema="geopaysages")
    op.drop_column("t_site", "legend_site", schema="geopaysages")
    op.drop_column("t_site", "testim_site", schema="geopaysages")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "t_site",
        sa.Column("legend_site", sa.VARCHAR(), autoincrement=False, nullable=True),
        schema="geopaysages",
    )
    op.add_column(
        "t_site",
        sa.Column("desc_site", sa.VARCHAR(), autoincrement=False, nullable=True),
        schema="geopaysages",
    )
    op.add_column(
        "t_site",
        sa.Column("testim_site", sa.VARCHAR(), autoincrement=False, nullable=True),
        schema="geopaysages",
    )
    op.add_column(
        "t_site",
        sa.Column("name_site", sa.VARCHAR(), autoincrement=False, nullable=True),
        schema="geopaysages",
    )
    op.add_column(
        "t_site",
        sa.Column("publish_site", sa.BOOLEAN(), autoincrement=False, nullable=True),
        schema="geopaysages",
    )
    op.add_column(
        "t_observatory",
        sa.Column("is_published", sa.BOOLEAN(), autoincrement=False, nullable=True),
        schema="geopaysages",
    )
    op.add_column(
        "t_observatory",
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True),
        schema="geopaysages",
    )
    op.add_column(
        "dico_theme",
        sa.Column("name_theme", sa.VARCHAR(), autoincrement=False, nullable=True),
        schema="geopaysages",
    )
    op.add_column(
        "dico_stheme",
        sa.Column("name_stheme", sa.VARCHAR(), autoincrement=False, nullable=True),
        schema="geopaysages",
    )
    op.add_column(
        "communes",
        sa.Column("nom_commune", sa.VARCHAR(), autoincrement=False, nullable=True),
        schema="geopaysages",
    )

    # populate
    op.execute(
        sa.text(
            """
        UPDATE geopaysages.communes c 
        SET nom_commune = (
            SELECT ct.nom_commune 
            FROM geopaysages.communes_translation ct 
            WHERE ct.row_id = c.code_commune AND ct.lang_id = 'fr'
        )
    """
        )
    )

    op.execute(
        sa.text(
            """
        UPDATE geopaysages.dico_stheme d 
        SET name_stheme = (
            SELECT dt.name_stheme 
            FROM geopaysages.dico_stheme_translation dt 
            WHERE d.id_stheme = dt.row_id AND dt.lang_id = 'fr'
        )
    """
        )
    )

    op.execute(
        sa.text(
            """
        UPDATE geopaysages.dico_theme d 
        SET name_theme = (
            SELECT dt.name_theme 
            FROM geopaysages.dico_theme_translation dt 
            WHERE d.id_theme = dt.row_id AND dt.lang_id = 'fr'
        )
    """
        )
    )

    op.execute(
        sa.text(
            """
        UPDATE geopaysages.t_observatory o 
        SET 
            title = (
                SELECT ot.title 
                FROM geopaysages.t_observatory_translation ot 
                WHERE o.id = ot.row_id AND ot.lang_id = 'fr'
            ),
            is_published = (
                SELECT ot.is_published 
                FROM geopaysages.t_observatory_translation ot 
                WHERE o.id = ot.row_id AND ot.lang_id = 'fr'
            )
    """
        )
    )

    op.execute(
        sa.text(
            """
        UPDATE geopaysages.t_site s 
        SET 
            legend_site = (
                SELECT st.legend_site 
                FROM geopaysages.t_site_translation st 
                WHERE s.id_site = st.row_id AND st.lang_id = 'fr'
            ),
            desc_site = (
                SELECT st.desc_site 
                FROM geopaysages.t_site_translation st 
                WHERE s.id_site = st.row_id AND st.lang_id = 'fr'
            ),
            testim_site = (
                SELECT st.testim_site 
                FROM geopaysages.t_site_translation st 
                WHERE s.id_site = st.row_id AND st.lang_id = 'fr'
            ),
            name_site = (
                SELECT st.name_site 
                FROM geopaysages.t_site_translation st 
                WHERE s.id_site = st.row_id AND st.lang_id = 'fr'
            ),
            publish_site = (
                SELECT st.publish_site 
                FROM geopaysages.t_site_translation st 
                WHERE s.id_site = st.row_id AND st.lang_id = 'fr'
            )
    """
        )
    )

    op.drop_table("t_site_translation", schema="geopaysages")
    op.drop_table("t_observatory_translation", schema="geopaysages")
    op.drop_table("dico_theme_translation", schema="geopaysages")
    op.drop_table("dico_stheme_translation", schema="geopaysages")
    op.drop_table("communes_translation", schema="geopaysages")
    op.drop_table("lang", schema="geopaysages")
    # ### end Alembic commands ###
