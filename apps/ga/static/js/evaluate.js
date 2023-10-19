/*
{% extends 'base.html' %}

{% block content %}
<div class="container p-4">
    <h3 class="mb-4">RATE THE MELODIES FROM 0 TO 5 STARS</h3>

    <div class="row">
        {% for melody in melodies %}
        <div class="col-md-4 mb-4">
            <div class="card">
                <img src="{{ melody.image.url }}" class="card-img-top" alt="Melody Image">
                <div class="card-body">
                    <h5 class="card-title">{{ melody.title }}</h5>
                    <p class="card-text">Average Rating: <span class="average-ratings">{{ melody.average_ratings }}</span></p>
                    <audio controls>
                        <source src="{{ melody.melody.url }}" type="audio/mpeg">
                    </audio>
                    <form class="rate-form mt-2" data-melody-id="{{ melody.id }}">
                        {% csrf_token %}
                        <select name="rating" class="form-control">
                            <option value="0">0 Stars</option>
                            <option value="1">1 Star</option>
                            <option value="2">2 Stars</option>
                            <option value="3">3 Stars</option>
                            <option value="4">4 Stars</option>
                            <option value="5">5 Stars</option>
                        </select>
                        <button type="button" class="btn btn-outline-success mt-2 rate-button">Submit Rating</button>
                    </form>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<script>
    // Agrega este código JavaScript para manejar las calificaciones de forma asíncrona
    document.addEventListener("DOMContentLoaded", function () {
        const rateButtons = document.querySelectorAll(".rate-button");
        rateButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                const form = this.closest(".rate-form");
                const melodyId = form.getAttribute("data-melody-id");
                const formData = new FormData(form);

                fetch(`evaluate/${melodyId}/`, {
                    method: "POST",
                    body: formData,
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            // Actualiza la calificación promedio en la tarjeta
                            const averageRatingSpan = form.querySelector(".average-ratings");
                            averageRatingSpan.textContent = data.average_rating;
                        } else {
                            // Muestra un mensaje de error si la calificación falla
                            alert("An error occurred while evaluating music: " + data.error_message);
                        }
                    })
                    .catch((error) => {
                        console.error("Error:", error);
                        alert("An error occurred while evaluating music ajajajaja.");
                    });
            });
        });
    });
</script>
{% endblock %}
*/