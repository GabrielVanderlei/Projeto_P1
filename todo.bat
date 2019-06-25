@SET original_cd=%cd%
@cd %~dp0
@python agenda.py %*
@cd %original_cd%