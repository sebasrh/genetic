from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from algorithm.gen_alg import algorithm_args, generate_population, evolve_population
from algorithm.representation import representation
from algorithm.main import main
from .models import GeneratedMusic, Evaluation
from django.http import JsonResponse
import os
import pickle
import json
import requests


def generate_image():
    url = "https://stablediffusionapi.com/api/v3/text2img"
    
    payload = json.dumps({
        'key': 'wtovAdcRL3LGYNgypE3PBNWo9feNL36AFZ7oVqWFPQdlp1Su1Q4F0bgK0zUG',
        "prompt": "RPG video game cover in pixel art",
        "negative_prompt": None,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "seed": None,
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "embeddings_model": None,
        "webhook": None,
        "track_id": None 
    })

    headers = {
        'Content-Type': 'application/json',
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        data = response.json()
        print(data)
        # Devuelve la URL de la imagen generada
        if data['status'] == 'success':
            return data['output'][0] if 'output' in data else None
    
    except requests.exceptions.RequestException as e:
        # Manejar errores de solicitud, por ejemplo, problemas de red
        print(e)
        return None


def save_population(population, generated_music):
    # Carpeta para guardar los archivos
    folder = f"algorithm/midi_out/{generated_music.id}"

    # Si la carpeta no existe, crearla
    if not os.path.exists(folder):
        os.mkdir(folder)

    # Nombre del archivo pickle
    file_name = f"{folder}/population_{generated_music.generation_number}.pkl"

    # Guardar la población en un archivo pickle
    with open(file_name, "wb") as file:
        pickle.dump(population, file)

    # Nombre del archivo txt
    file_name = f"{folder}/population_{generated_music.generation_number}.txt"

    # Guardar la población en archivos de texto
    with open(file_name, "w") as file:
        for melody in population:
            file.write(str(melody) + "\n")


def load_population(generated_music):
    # Carpeta para cargar los archivos
    folder = f"algorithm/midi_out/{generated_music.id}"

    # Nombre del archivo pickle
    file_name = f"{folder}/population_{generated_music.generation_number}.pkl"

    # Cargar la población desde el archivo pickle
    with open(file_name, "rb") as file:
        population = pickle.load(file)

    return population


@login_required
def ga(request):
    user = request.user
    if user.is_superuser and request.method == 'POST':

        generated_music = main()

        args_1 = generated_music.musical_representation
        args_2 = generated_music.ga_info

        rep_obj = representation(args_1.key_signature, args_1.scale_signature, args_1.tempo,
                                 args_1.has_back_track, args_1.uses_arp_or_scale)

        alg_args = algorithm_args(args_2.population_size,
                                  args_2.num_generations, args_2.num_selected, args_2.num_children, args_2.crossover_probability, args_2.mutation_probability)

        # Generar la población inicial
        population = generate_population(rep_obj, alg_args)

        # generar melodias
        for melody in population:
            representation.generate_melody(rep_obj, melody, generated_music)

        # Guardar la población inicial
        save_population(population, generated_music)

        # Calcular la duración de la música generada
        generated_music.duration = generated_music.calculate_duration()

        # Generar la imagen
        image_url = generate_image()

        # Descargar la imagen 
        response = requests.get(image_url)

        # Guardar la imagen en la carpeta media
        if response.status_code == 200:
            with open(f"media/img/image_{generated_music.id}.jpg", "wb") as f:
                f.write(response.content)

        # Asignar la imagen a la música generada
        image = f"img/image_{generated_music.id}.jpg"

        generated_music.img = image

        # Guardar la música generada
        generated_music.save()

        return redirect('ga')
    else:
        generations = GeneratedMusic.objects.all().order_by('-created_at')
        return render(request, 'ga.html', {'generations': generations, 'user': user})

@login_required
def generations(request, generations_id):
    user = request.user

    # Obtén el objeto GeneratedMusic por su clave primaria (id)
    generated_music = get_object_or_404(GeneratedMusic, pk=generations_id)

    # Obtener la última generación de melodías
    latest_generation = generated_music.melodies.filter(
        generation=generated_music.generation_number).order_by('created_at')

    # Consultar para obtener las calificaciones del usuario actual
    user_ratings = Evaluation.objects.filter(
        user=user, melody__in=latest_generation)

    user_ratings_data = {}  # Un diccionario para almacenar los datos de calificación

    # Iterar sobre las calificaciones del usuario y almacenarlas en el diccionario
    for rating in user_ratings:
        user_ratings_data[rating.melody.id] = rating.rating

    user_ratings_json = json.dumps(user_ratings_data)  # Convertir a JSON

    # Verificar si el usuario ya ha calificado las melodías
    for melody in latest_generation:
        melody.user_has_rated = melody.user_has_rated(user)

    return render(request, 'generations.html', {'melodies': latest_generation, 'user_ratings': user_ratings_json, 'user': user, 'generated_music': generated_music})


@login_required
def evaluate(request, generations_id, melody_id):
    user = request.user
    if request.method == 'POST':
        try:
            # Obtener el objeto GeneratedMusic por su clave primaria (id)
            generated_music = GeneratedMusic.objects.get(pk=generations_id)

            # Obtener el objeto Melody por su clave primaria (id)
            melody = generated_music.melodies.get(pk=melody_id)

            # Verifica si el usuario ya ha calificado esta melodía
            if melody.user_has_rated(user):
                response_data = {
                    'success': False,
                    'error_message': 'El usuario ya ha calificado esta melodía.'
                }
                return JsonResponse(response_data, status=400)

            else:
                # Obtener la calificación del usuario
                rating = request.POST.get('ratings')

                # Crear una nueva calificación
                evaluation = Evaluation(
                    user=user, melody=melody, rating=rating)
                evaluation.save()

                # Agregar la calificación a la melodía
                melody.user_rating.add(evaluation)

                # Actualizar la calificación promedio de la melodía
                melody.average_users_ratings()

                response_data = {
                    'success': True,
                    'average_rating': melody.average_ratings,
                    'users_ratings_count': melody.user_rating.all().count()
                }
                # Registro de éxito
                return JsonResponse(response_data, status=200)

        except Exception as e:
            response_data = {
                'success': False,
                'error_message': str(e)
            }
            return JsonResponse(response_data, status=400)


@login_required
def evolve(request, generations_id):
    user = request.user
    if user.is_superuser and request.method == 'POST':
        try:
            # Obtener el objeto GeneratedMusic por su clave primaria (id)
            generated_music = get_object_or_404(
                GeneratedMusic, pk=generations_id)

            # Verificar si el número de generación actual es mayor que el número total de generaciones
            if generated_music.generation_number > generated_music.ga_info.num_generations:
                response_data = {
                    'success': False,
                    'error_message': 'The number of generations has been reached'
                }
                return JsonResponse(response_data, status=400)

            # Si el número de generación actual es menor que el número total de generaciones, evolucionar
            else:
                args_1 = generated_music.musical_representation
                args_2 = generated_music.ga_info

                rep_obj = representation(args_1.key_signature, args_1.scale_signature, args_1.tempo,
                                         args_1.has_back_track, args_1.uses_arp_or_scale)

                alg_args = algorithm_args(args_2.population_size,
                                          args_2.num_generations, args_2.num_selected, args_2.num_children, args_2.crossover_probability, args_2.mutation_probability)

                # Cargar la población actual
                population = load_population(generated_music)

                # Obtener todas las melodías
                mels = generated_music.melodies.all()

                # Lista de promedios de calificaciones de melodías en mels (GeneratedMelody)
                avg_ratings = [mel.average_ratings for mel in mels]

                # Asignar el promedio de calificaciones como fitness a cada melodía en la población
                for ind, avg_rating in zip(population, avg_ratings):
                    ind.fitness.values = (avg_rating,)

                # Evolucionar la población actual y obtener la nueva población
                new_pop = evolve_population(population, alg_args)

                # Actualizar el número de generación
                generated_music.increase_generation_number()

                # generar melodias
                for melody in new_pop:
                    representation.generate_melody(
                        rep_obj, melody, generated_music)

                # Guardar la nueva población
                save_population(new_pop, generated_music)

                return redirect('generations', generations_id=generations_id)
        except Exception as e:
            # Manejar errores adecuadamente y mostrar mensajes de error
            response_data = {
                'success': False,
                'error_message': str(e)
            }
            return JsonResponse(response_data, status=400)
