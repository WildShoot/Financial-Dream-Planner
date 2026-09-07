const form = document.getElementById("plannerForm");
form.addEventListener("submit", async function(event) {
    event.preventDefault();
    const data = {

        name: document.getElementById("name").value,
        age: Number(
            document.getElementById("age").value
        ),

        city: document.getElementById("city").value,

        education: document.getElementById("education").value,

        job_role: document.getElementById("job_role").value,

        saving_percentage: Number(
            document.getElementById("saving_percentage").value
        ),

        marriage_years: Number(
            document.getElementById("marriage_years").value
        ),

        car_years: Number(
            document.getElementById("car_years").value
        ),

        home_years: Number(
            document.getElementById("home_years").value
        )

    };


    try {

        const response = await fetch("/plan", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(data)

        });


        const result = await response.json();


        displayResult(result);

    }

    catch (error) {

        console.error(error);

        alert("Error connecting to the server!");

    }

});


function displayResult(data) {


    const resultDiv = document.getElementById("result");

    const content = document.getElementById("resultContent");


    resultDiv.classList.remove("hidden");


    let html = `

        <p><strong>Name:</strong> ${data.user_name}</p>

        <p>
            <strong>Predicted Monthly Salary:</strong>
            ₹${data.predicted_monthly_salary}
        </p>

        <p>
            <strong>Saving Percentage:</strong>
            ${data.saving_percentage}%
        </p>

        <p>
            <strong>Monthly Investment Capacity:</strong>
            ₹${data.monthly_investment_capacity}
        </p>

        <p>
            <strong>Total Monthly Investment Required:</strong>
            ₹${data.total_monthly_investment_required}
        </p>

        <p>
            <strong>Overall Status:</strong>
            ${data.overall_status}
        </p>

        <p>
            <strong>Suggestion:</strong>
            ${data.suggestion}
        </p>

        <hr>

        <h2>Goal Details</h2>

    `;


    for (let goal in data.goals) {


        const item = data.goals[goal];


        html += `

            <div class="goal-card">

                <h3>${goal}</h3>

                <p>
                    <strong>Timeline:</strong>
                    ${item.timeline_years} years
                </p>

                <p>
                    <strong>Current Cost:</strong>
                    ₹${item.current_cost}
                </p>

                <p>
                    <strong>Future Cost:</strong>
                    ₹${item.future_cost}
                </p>

                <p>
                    <strong>Monthly Investment Required:</strong>
                    ₹${item.monthly_investment_required}
                </p>

                <p>
                    <strong>Investment Category:</strong>
                    ${item.investment_category}
                </p>

                <p>
                    <strong>Status:</strong>
                    ${item.status}
                </p>

            </div>

        `;

    }


    content.innerHTML = html;

}



async function askQuestion() {


    const question = document.getElementById("question").value;


    if (!question) {

        alert("Please enter a question!");

        return;

    }


    try {


        const response = await fetch("/ask", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                question: question

            })

        });


        const result = await response.json();


        document.getElementById("ragResult").innerHTML = `

            <h3>Answer</h3>

            <p>${result.answer}</p>

            <br>

            <strong>Source:</strong>

            ${result.source || "No source found"}

        `;


    }

    catch (error) {


        console.error(error);

        alert("Error connecting to Financial Assistant!");

    }

}
