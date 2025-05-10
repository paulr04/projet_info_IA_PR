from objects import Reservation_DSL

bad_dsl = "RESERVATION 123 CLIENT 456 VEHICULE 123 DU 01-01-2025 AU 02-01-2025 JOURS 2 PRIX 50 SURCLASSEMENT False"

resa_dsl = Reservation_DSL.from_dsl(bad_dsl) 