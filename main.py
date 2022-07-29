from classes import CampoMinado

campo = CampoMinado(10, 10, 0.2)
campo.cria_bombas()
# campo.mostra_campo(campo.campo_minado)
campo.conta_bombas()
campo.mostra_campo(campo.campo_minado)
campo.escolha(2, 5)
campo.escolha(9, 9)
campo.escolha(6, 0)
campo.escolha(9, 0)
campo.escolha(2, 0)
# campo.escolha(7, 0)
campo.mostra_campo()
