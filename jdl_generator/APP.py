import os

def generate_app_jdl(
  application_type="monolith",
  authentication_type="jwt",
  base_name="sampleApp",
  build_tool="maven",
  cache_provider="ehcache",
  client_framework="angular",
  client_package_manager="npm",
  client_theme=None,  # se for "none", não aparece
  client_theme_variant=None,
  database_type="sql",
  dev_database_type="h2Disk",
  dto_suffix="DTO",
  enable_hibernate_cache=True,
  enable_swagger_codegen=False,
  enable_translation=True,
  entity_suffix="Entity",
  jhi_prefix="jhi",
  languages=None,
  message_broker="no",
  native_language="en",
  package_name="com.example.myapp",
  prod_database_type="mysql",
  reactive=False,
  search_engine="elasticsearch",
  server_port=8080,
  service_discovery_type="no",
  skip_client=False,
  skip_server=False,
  skip_user_management=False,
  test_frameworks=None,
  websocket="no"
):
  """
  Gera o bloco de application { config { ... } } ignorando parâmetros cujo valor é None
  ou que sejam explicitamente a string "none" (em qualquer capitalização).
  Dessa forma, linhas como "clientTheme none" não aparecem no JDL.
  """

  if languages is None:
      languages = ["en", "fr"]  # valor padrão

  if test_frameworks is None:
      test_frameworks = ["cucumber", "protractor", "jest"]  # valor padrão

  config_params = {
      "applicationType": application_type,
      "authenticationType": authentication_type,
      "baseName": base_name,
      "buildTool": build_tool,
      "cacheProvider": cache_provider,
      "clientFramework": client_framework,
      "clientPackageManager": client_package_manager,
      "clientTheme": client_theme,
      "clientThemeVariant": client_theme_variant,
      "databaseType": database_type,
      "devDatabaseType": dev_database_type,
      "dtoSuffix": dto_suffix,
      "enableHibernateCache": str(enable_hibernate_cache).lower(),
      "enableSwaggerCodegen": str(enable_swagger_codegen).lower(),
      "enableTranslation": str(enable_translation).lower(),
      "entitySuffix": entity_suffix,
      "jhiPrefix": jhi_prefix,
      "languages": f"[{', '.join(languages)}]" if languages else None,
      "messageBroker": message_broker,
      "nativeLanguage": native_language,
      "packageName": package_name,
      "prodDatabaseType": prod_database_type,
      "reactive": str(reactive).lower(),
      "searchEngine": search_engine,
      "serverPort": server_port,
      "serviceDiscoveryType": service_discovery_type,
      "skipClient": str(skip_client).lower(),
      "skipServer": str(skip_server).lower(),
      "skipUserManagement": str(skip_user_management).lower(),
      "testFrameworks": f"[{', '.join(test_frameworks)}]" if test_frameworks else None,
      "websocket": websocket
  }

  lines = []
  lines.append("application {")
  lines.append("  config {")

  for key, value in config_params.items():
      # Se for None ou string "none" (ignorando maiúsculas/minúsculas), pula a linha
      if value is None or (isinstance(value, str) and value.lower() == "none"):
          continue
      lines.append(f"    {key} {value}")

  lines.append("  }")
  lines.append("}")

  return "\n".join(lines) + "\n"

def main():
  base_dir = os.path.dirname(os.path.abspath(__file__))
  output_file = os.path.join(base_dir, "APP.jdl")

  jdl_content = generate_app_jdl()
  with open(output_file, "w", encoding="utf-8") as f:
      f.write(jdl_content)

  print(f"Arquivo 'APP.jdl' gerado/atualizado!")

if __name__ == "__main__":
  main()
