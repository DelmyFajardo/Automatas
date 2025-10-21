import argparse
from motor_generacion import generar_por_parametros
import palabras_generadas_db


def main():
    parser = argparse.ArgumentParser(description='Generar y almacenar elementos (contraseñas, correos, direcciones, teléfonos, usuarios)')
    parser.add_argument('--contrasenas', type=int, default=0, help='Número de contraseñas a generar')
    parser.add_argument('--correos', type=int, default=0, help='Número de correos a generar')
    parser.add_argument('--direcciones', type=int, default=0, help='Número de direcciones a generar')
    parser.add_argument('--telefonos', type=int, default=0, help='Número de teléfonos a generar')
    parser.add_argument('--usuarios', type=int, default=0, help='Número de usuarios a generar')
    parser.add_argument('--no-save', dest='save', action='store_false', help='No guardar en la base de datos')
    parser.set_defaults(save=True)

    args = parser.parse_args()
    palabras_generadas_db.crear_tablas()

    parametros = {
        'contraseña': args.contrasenas,
        'correo': args.correos,
        'direccion': args.direcciones,
        'telefono': args.telefonos,
        'usuario': args.usuarios,
    }

    print('Generando...')
    resultados = generar_por_parametros(parametros, save=args.save)

    print('Resultado:')
    for k, v in resultados.items():
        print(f"{k}: {v}")


if __name__ == '__main__':
    main()
