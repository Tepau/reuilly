from .ping.models import Cotisation, Competition, Saison
cotisation1 = Cotisation.objects.create(nom="fille -11ans", prix=50, description="fille -11ans")
cotisation2 = Cotisation.objects.create(nom="enfant -11ans", prix=140, description="enfant -11ans")
cotisation3 = Cotisation.objects.create(nom="enfant +11ans", prix=155, description="enfant +11ans")
cotisation4 = Cotisation.objects.create(nom="adulte competition", prix=155, description="adulte competition")
cotisation5 = Cotisation.objects.create(nom="adulte loisir", prix=145, description="adulte loisir")

# Création de 2 compet
competition1 = Competition.objects.create(nom="indivs", prix=41, description="criterium fédéral")
competition2 = Competition.objects.create(nom="fscf", prix=25, description="compet de touriste")

saison1 = Saison.objects.create(date_debut_saison="2019-08-01", date_fin_saison="2020-07-31", nom='2019/2020')
saison2 = Saison.objects.create(date_debut_saison="2020-08-01", date_fin_saison="2021-07-31", nom='2020/2021')
saison3 = Saison.objects.create(date_debut_saison="2021-08-01", date_fin_saison="2022-07-31", nom='2021/2022')
saison4 = Saison.objects.create(date_debut_saison="2022-08-01", date_fin_saison="2023-07-31", nom='2022/2023')
saison5 = Saison.objects.create(date_debut_saison="2023-08-01", date_fin_saison="2024-07-31", nom='2023/2024')
saison6 = Saison.objects.create(date_debut_saison="2024-08-01", date_fin_saison="2025-07-31", nom='2024/2025')
saison7 = Saison.objects.create(date_debut_saison="2025-08-01", date_fin_saison="2026-07-31", nom='2025/2026')
saison8 = Saison.objects.create(date_debut_saison="2026-08-01", date_fin_saison="2027-07-31", nom='2026/2027')
saison9 = Saison.objects.create(date_debut_saison="2027-08-01", date_fin_saison="2028-07-31", nom='2027/2028')

