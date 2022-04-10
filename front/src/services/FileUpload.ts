import http from "./http"

type Image = {
    task_id: string
    id: string
    url: string
    gray_id?: string
    gray_url?: string
}

export function toGray(data: Image): Promise<any> {
    return http.post("/gray_scale", data)
}
