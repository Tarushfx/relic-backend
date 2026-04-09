from rest_framework.renderers import JSONRenderer


class CoreJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response")
        status_code = response.status_code
        if 200 <= status_code < 400:
            if isinstance(data, dict) and all(
                k in data for k in ("success", "code", "message", "data", "errors")
            ):
                return super().render(data, accepted_media_type, renderer_context)

            standardized_data = {
                "success": True,
                "code": status_code,
                "message": "Operation successful",
                "data": data,
                "errors": None,
            }
            return super().render(
                standardized_data, accepted_media_type, renderer_context
            )
        # info: error responses are handled by the custom exception handler, so we just render them as they are
        return super().render(data, accepted_media_type, renderer_context)
