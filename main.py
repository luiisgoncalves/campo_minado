from classes import CampoMinado

campo = CampoMinado(10, 10, 0.1)
campo.cria_bombas()
campo.mostra_campo(campo.campo_minado)
campo.conta_bombas()
print()
campo.mostra_campo(campo.campo_minado)
