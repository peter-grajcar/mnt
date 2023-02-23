
const main = document.getElementById("main")

fetch("https://peter-grajcar.github.io/mnt/news.json", {method: 'get', mode: 'cors'})
    .then((response) => response.text())
    .then((text) => {
        const json = '{ "data": ' + text + '}'
        const data = JSON.parse(json)["data"]

        main.innerHTML = ""

        let i = 0
        for (x of data) {
            ++i
            if (i > 100)
                break

            if (!x["new_content"])
                continue

            const divider = document.createElement("div")
            divider.classList.add("divider")
            const article = document.createElement("div")
            article.classList.add("article")
            const header = document.createElement("div", { "class": "" })
            header.classList.add("article-header")
            const body = document.createElement("div")
            body.classList.add("body")
            const time = document.createElement("span")
            time.classList.add("article-time")
            const link = document.createElement("a")
            link.classList.add("article-link-to-original")
            link.setAttribute("href", x["link"])
            const paragraph = document.createElement("p")

            time.innerText = x["time"]
            link.innerText = "pôvodná správa"
            paragraph.innerHTML = x["new_content"]
            divider.innerHTML = "&#9672; &#9672; &#9672;"


            link.addEventListener("click", (e) => {
                if (!confirm("Počuj, priateľu, tento odkaz ťa môže vniesť do hlbín mora negativity. Si si istý, že chceš podstúpiť toto riziko?"))
                    e.preventDefault()
            })

            header.appendChild(time)
            header.appendChild(link)
            body.appendChild(paragraph)
            article.appendChild(header)
            article.appendChild(body)
            main.appendChild(article)
            main.appendChild(divider)
        }
    })
    .catch((error) => {
        main.innerText = "Z ľútosťou Vám oznamujeme, že minúta pomunila. Skúste to prosím neskôr."
        console.error(error)
    })

