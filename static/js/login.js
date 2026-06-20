function alternarSenha() {
    const campoSenha = document.getElementById('senha');
    campoSenha.type = campoSenha.type === 'password' ? 'text' : 'password';
}