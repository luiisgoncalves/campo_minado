from test import CampoMinado

campo = CampoMinado(10, 10, 0.1)
campo.mostra_campo()
campo.cria_bombas()
campo.mostra_campo(campo.campo_minado)
