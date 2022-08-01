from classes import CampoMinado

campo = CampoMinado(15, 15, 0.2)
campo.cria_bombas()
# campo.mostra_campo(campo.campo_minado)
campo.conta_bombas()
campo.mostra_campo(campo.campo_minado)

campo.escolha(3, 3)
# campo.escolha(9, 9)
# campo.escolha(6, 0)
# campo.escolha(9, 0)
# campo.escolha(2, 0)
# campo.escolha(7, 0)
campo.mostra_campo()
