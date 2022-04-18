import http from "./http"

type Image = {
    task_id: string
    id: string
    url: string
    gray_id?: string
    gray_url?: string
    threshold?: number
}

export function toGray(data: Image): Promise<any> {
    const postData = {
        task_id: data.task_id,
        id:data.id
    }
    return http.post("/gray_scale", postData)
}

export function binarize(data: Image): Promise<any> {
    const postData = {
        task_id: data.task_id,
        id:data.id,
        threshold:data.threshold
    }
    return http.post("/binarize", postData)
}
