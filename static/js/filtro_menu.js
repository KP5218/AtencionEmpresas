 document.addEventListener("DOMContentLoaded", function() {
            // Función para verificar si un elemento ya existe en la lista de navegación
            function checkIfExists(element) {
                var links = document.querySelectorAll(".nav-item a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].getAttribute("href") === element.getAttribute("href")) {
                        return true;
                    }
                }
                return false;
            }

            // Enlace para "Agendar hora"
            var agendarLink = document.createElement("a");
            agendarLink.setAttribute("href", "/agendar/");
            agendarLink.textContent = "Agendar hora";
            agendarLink.classList.add("nav-link", "text-light", "fw-bold");

            // Enlace para "Lista de agenda"
            var listaLink = document.createElement("a");
            listaLink.setAttribute("href", "/lista_horas/");
            listaLink.textContent = "Lista de agenda";
            listaLink.classList.add("nav-link", "text-light", "fw-bold");

            // Verificar si los enlaces ya existen antes de agregarlos
            if (!checkIfExists(agendarLink)) {
                var liAgendar = document.createElement("li");
                liAgendar.classList.add("nav-item");
                liAgendar.appendChild(agendarLink);
                document.querySelector(".card-header ul").appendChild(liAgendar);
            }

            if (!checkIfExists(listaLink)) {
                var liLista = document.createElement("li");
                liLista.classList.add("nav-item");
                liLista.appendChild(listaLink);
                document.querySelector(".card-header ul").appendChild(liLista);
            }
        });