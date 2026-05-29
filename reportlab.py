
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


# ==================================================
# Création des graphiques
# ==================================================

plt.figure(figsize=(6,4))
sns.histplot(dataset["Age"], kde=True)
plt.title("Distribution de l'âge")
plt.tight_layout()
plt.savefig("age_hist.png")
plt.close()

plt.figure(figsize=(6,4))
sns.countplot(data=dataset, x="Churn")
plt.title("Répartition du churn")
plt.tight_layout()
plt.savefig("churn_count.png")
plt.close()

# ==================================================
# Construction du PDF
# ==================================================

doc = SimpleDocTemplate("rapport_churn.pdf")

styles = getSampleStyleSheet()

elements = []

# ==================================================
# Page de garde
# ==================================================

elements.append(
    Paragraph(
        "Rapport d'analyse du churn",
        styles["Title"]
    )
)

elements.append(
    Paragraph(
        """
        Ce rapport présente une analyse exploratoire des données clients
        dans le but d'identifier les principaux facteurs susceptibles
        d'influencer le churn. Les indicateurs statistiques et les
        visualisations présentés dans ce document permettent de mieux
        comprendre la structure de la population étudiée ainsi que la
        répartition des comportements de résiliation observés.
        """,
        styles["BodyText"]
    )
)

elements.append(Spacer(1, 30))


# ==================================================
# Description du dataset
# ==================================================

elements.append(
    Paragraph(
        "Description du dataset",
        styles["Heading1"]
    )
)

elements.append(
    Paragraph(
        f"Nombre de lignes : {dataset.shape[0]}",
        styles["Normal"]
    )
)

elements.append(
    Paragraph(
        f"Nombre de colonnes : {dataset.shape[1]}",
        styles["Normal"]
    )
)

elements.append(Spacer(1, 20))

# ==================================================
# Statistiques descriptives
# ==================================================

elements.append(
    Paragraph(
        "Statistiques descriptives",
        styles["Heading1"]
    )
)

stats = dataset.describe().round(2)

table_data = [
    ["Statistique"] + list(stats.columns)
]

for index in stats.index:
    table_data.append(
        [index] + stats.loc[index].tolist()
    )

table = Table(table_data)

table.setStyle(
    TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ROWBACKGROUNDS',
         (0,1),
         (-1,-1),
         [colors.whitesmoke,
          colors.lightgrey])
    ])
)

elements.append(table)

elements.append(PageBreak())

# ==================================================
# Visualisation 1
# ==================================================

elements.append(
    Paragraph(
        "Distribution de l'âge",
        styles["Heading1"]
    )
)

elements.append(
    Image(
        "age_hist.png",
        width=400,
        height=250
    )
)



# ==================================================
# Visualisation 2
# ==================================================

elements.append(
    Paragraph(
        "Analyse du churn",
        styles["Heading1"]
    )
)

elements.append(
    Image(
        "churn_count.png",
        width=400,
        height=250
    )
)

elements.append(PageBreak())

# ==================================================
# Synthèse
# ==================================================

elements.append(
    Paragraph(
        "Synthèse",
        styles["Heading1"]
    )
)

elements.append(
    Paragraph(
        f"""
        Le dataset contient {len(dataset)} clients, parmi lesquels
        {100 * dataset['Churn'].value_counts(normalize=True).get(1,0):.1f} %
        ont quitté l'entreprise. Les premières analyses mettent en évidence
        des différences marquées entre les clients ayant résilié et ceux
        ayant conservé leurs services. Le nombre de sites visités, l'ancienneté
        ainsi que l'âge semblent être des variables très déterminantes dans le
        churn

        Ces observations permettent d'orienter les actions de rétention vers
        les populations les plus exposées. Elles soulignent notamment
        l'importance des dispositifs d'accompagnement des nouveaux clients,
        du développement de l'équipement multi-services et de la mise en
        place d'offres adaptées aux différents segments de clientèle.
        """
        ,
        styles["BodyText"]
    )
)

# ==================================================
# Génération du PDF
# ==================================================

doc.build(elements)

print("rapport_churn.pdf généré avec succès")
