console.log("JS working");
const url = window.location.href

const quizBox = document.getElementById('quiz-box')

$.ajax({
    type: "GET",
    url: `${url}questions/`,
    success: function(response) {
        console.log(response)
        const data = response.data
        data.forEach(question => {
            // for (const [question, choices] of Object.entries(qs)){
            //     console.log(question)
            //     console.log(choices)
            //     quizBox.innerHTML += `
            //         <hr>
            //         <div>
            //             <b>${question}</b>
            //         </div>
            //     `
            // }
            quizBox.innerHTML += `
                <hr>
                <div>
                    <b>${question.qs}</b>
                    <br>
                    <input type="radio" class="ans" id="${question.qs}-${question.op1}" name="${question.qs}" value="${question.op1}">
                    <label for="${question.qs}-${question.op1}">${question.op1}</label>
                    <br>
                    <input type="radio" class="ans" id="${question.qs}-${question.op2}" name="${question.qs}" value="${question.op2}">
                    <label for="${question.qs}-${question.op2}">${question.op2}</label>
                    <br>
                    <input type="radio" class="ans" id=${question.qs}-${question.op3} name="${question.qs}" value="${question.op3}">
                    <label for="${question.qs}-${question.op3}">${question.op3}</label>
                    <br>
                    <input type="radio" class="ans" id="${question.qs}-${question.op4}" name="${question.qs}" value="${question.op4}">
                    <label for="${question.qs}-${question.op4}">${question.op4}</label>
                </div>
            `
        });
    },
    error: function(error) {
        console.log(error)
    }
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
    const elements = [...document.getElementsByClassName("ans")]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value,
    elements.forEach(element => {
        if(element.checked) {
            data[element.name] = element.value
        } else {
            if (!data[element.name]) {
                data[element.name] = null
            }
        }
    })

    $.ajax({
        type:"POST",
        url: `${url}save/`,
        data: data,
        success: function(response) {
            console.log(response)
            window.location.href=`http://127.0.0.1:8000/course/${response.course_pk}/st_exam/${response.pk}/`
        },
        error: function(error) {
            console.log(error)
        }
    })
}

quizForm.addEventListener('submit', e=>{
    e.preventDefault()

    sendData()

})